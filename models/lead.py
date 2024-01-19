# Copyright 2020 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    document_ids = fields.One2many(
        string="Documents",
        comodel_name="ir.attachment",
        compute="_compute_document_ids",
    )
    documents_count = fields.Integer(
        compute="_compute_document_ids",
        string="Document Count",
    )

    def _compute_document_ids(self):
        IrAttachment = self.env["ir.attachment"]
        attachments = IrAttachment.search(
            [("res_model", "=", self._name), ("res_id", "in", self.ids)]
        )

        result = dict.fromkeys(self.ids, IrAttachment)
        for attachment in attachments:
            result[attachment.res_id] |= attachment

        for record in self:
            record.document_ids = result[record.id]
            record.documents_count = len(record.document_ids)

    def action_get_attachment_tree_view(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("base.action_attachment")
        action["context"] = {
            "default_res_model": self._name,
            "default_res_id": self.ids[0],
        }
        action["domain"] = str(
            [("res_model", "=", self._name), ("res_id", "in", self.ids)]
        )
        action["search_view_id"] = (
            self.env.ref("partner_document.ir_attachment_view_search").id,
        )
        return action
