# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import api, exceptions, fields, models, tools

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    auto_validate = fields.Boolean(
        compute="_compute_auto_validate",
        store=True,
    )

    @api.constrains("bom_id", "auto_validate", "product_qty")
    def check_bom_auto_validate(self):
        bypass_check = self.env.context.get("disable_check_mo_auto_validate")
        if bypass_check:
            return

        for mo in self:
            if mo.bom_id:
                qty_in_mo_uom = mo.bom_id.product_uom_id._compute_quantity(
                    mo.bom_id.product_qty, mo.product_uom_id
                )

                qty_ok = (
                    tools.float_compare(
                        mo.product_qty,
                        qty_in_mo_uom,
                        precision_rounding=mo.product_uom_id.rounding,
                    )
                    == 0
                )

                if mo.auto_validate and not qty_ok:
                    raise exceptions.ValidationError(
                        self.env._(
                            "The quantity to produce is restricted to %(qty)s %(uom)s "
                            "as the BoM is configured with the "
                            "'Order Auto Validation' option.",
                            qty=mo.bom_id.product_qty,
                            uom=mo.bom_id.product_uom_id.name,
                        )
                    )

    @api.depends("bom_id.mo_auto_validation", "state")
    def _compute_auto_validate(self):
        for prod in self:
            if prod.state != "draft":
                # Avoid recomputing the value once the MO is confirmed.
                # e.g. if the value changes on the BOM but the MO was already confirmed,
                # or if the user forces another value while the MO is in draft,
                # we don't want to change the value after confirmation.
                continue
            prod.auto_validate = prod.bom_id.mo_auto_validation

    def _auto_validate_after_picking(self):
        self.ensure_one()
        if self.state == "progress":
            # If the MO is already in progress, we want to call the immediate
            # wizard to handle lot/serial number automatically (if any).
            action = self._action_generate_immediate_wizard()
            self._handle_wiz_mrp_immediate_production(action)
        res = self.button_mark_done()
        if res is True:
            return True
        res = self.handle_mark_done_result(res)
        # Each call might return a new wizard, loop until we satisfy all of them
        while isinstance(res, dict):
            res = self.handle_mark_done_result(res)

    def handle_mark_done_result(self, res):
        if res["res_model"] == "mrp.production":
            # MO has been processed and returned an action to open a backorder
            return True
        handler_name = "_handle_wiz_" + res["res_model"].replace(".", "_")
        handler = getattr(self, handler_name, None)
        if not handler:
            _logger.warning("'%s' wizard is not supported", res["res_model"])
            return True
        return handler(res)

    def _handle_wiz_mrp_batch_produce(self, action):
        wiz_model = self.env[action["res_model"]].with_context(
            **action.get("context", {})
        )
        wiz = wiz_model.create({})
        wiz.action_generate_production_text()
        return wiz.action_done()

    def _handle_wiz_mrp_production_backorder(self, action):
        wiz_model = self.env[action["res_model"]].with_context(
            **action.get("context", {})
        )
        wiz = wiz_model.create({})
        return wiz.action_backorder()

    @api.model_create_multi
    def create(self, values_list):
        new_values_list, messages_to_post = self.adapt_values_qty_for_auto_validation(
            values_list
        )
        res = super().create(new_values_list)
        if messages_to_post:
            for pos, msg in messages_to_post.items():
                prod = res[pos]
                prod.message_post(body=msg)
        return res

    @api.model
    def adapt_values_qty_for_auto_validation(self, values_list):
        """Adapt create values according to qty with auto validated BOM

        If MOs are to be created with a BOM having auto validation, we must ensure
        the quantity of the MO is equal to the quantity of the BOM.
        However when MOs are created through procurements, the requested quantity
        is based on the procurement quantity, so we should either
          * increase the quantity to match the BOM if procurement value is lower
          * split the values to create one MO into multiple values to create multiple
          MOs matching the BOM quantity if procurement value is bigger
        """
        messages_to_post = {}
        if not self.env.context.get("_split_create_values_for_auto_validation"):
            return values_list, messages_to_post
        new_values_list = []
        for values in values_list:
            bom_id = values.get("bom_id")
            if not bom_id:
                new_values_list.append(values)
                continue
            bom = self.env["mrp.bom"].browse(bom_id)
            if not bom.mo_auto_validation:
                new_values_list.append(values)
                continue
            create_qty = values.get("product_qty")
            create_uom = self.env["uom.uom"].browse(values.get("product_uom_id"))
            bom_qty = bom.product_qty
            bom_uom = bom.product_uom_id
            if create_uom != bom_uom:
                create_qty = create_uom._compute_quantity(create_qty, bom_uom)
            if (
                tools.float_compare(
                    create_qty, bom_qty, precision_rounding=bom_uom.rounding
                )
                == 0
            ):
                new_values_list.append(values)
                continue
            elif (
                tools.float_compare(
                    create_qty, bom_qty, precision_rounding=bom_uom.rounding
                )
                < 0
            ):
                procure_qty = values.get("product_qty")
                values["product_qty"] = bom_qty
                values["product_uom_id"] = bom_uom.id
                msg = self.env._(
                    "Quantity in procurement (%(product_qty)s %(product_uom_name)s) "
                    "was increased to %(bom_qty)s %(bom_uom_name)s due to auto "
                    "validation feature preventing to create an MO with a different "
                    "qty than defined on the BOM.",
                    product_qty=procure_qty,
                    product_uom_name=create_uom.display_name,
                    bom_qty=bom_qty,
                    bom_uom_name=bom_uom.display_name,
                )
                messages_to_post[len(new_values_list)] = msg
                new_values_list.append(values)
                continue
            # If we get here we need to split the prepared MO values
            #  into multiple MO values to respect BOM qty
            while (
                tools.float_compare(create_qty, 0, precision_rounding=bom_uom.rounding)
                > 0
            ):
                new_values = values.copy()
                new_values["product_qty"] = bom_qty
                new_values["product_uom_id"] = bom_uom.id
                msg = self.env._(
                    "Quantity in procurement (%(product_qty)s %(product_uom_name)s) "
                    "was split to multiple production orders of %(bom_qty)s "
                    "%(bom_uom_name)s due to auto validation feature preventing to set "
                    "a quantity to produce different than the quantity defined "
                    "on the Bill of Materials.",
                    product_qty=values.get("product_qty"),
                    product_uom_name=create_uom.display_name,
                    bom_qty=bom_qty,
                    bom_uom_name=bom_uom.display_name,
                )
                messages_to_post[len(new_values_list)] = msg
                new_values_list.append(new_values)
                create_qty -= bom_qty
        return new_values_list, messages_to_post
