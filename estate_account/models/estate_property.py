from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        invoice = self.env['account.move'].sudo().create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
            'invoice_line_ids': [Command.create({'name': 'Available House 01', 'quantity': 1.0,
                                                 'price_unit': (6 * self.selling_price) / 100}),
                                 Command.create({'name': 'Administrative Fee', 'quantity': 1.0,
                                                 'price_unit': 100.0})]
        })
        return res
