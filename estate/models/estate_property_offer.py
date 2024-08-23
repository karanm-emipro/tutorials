from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="Price")
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, copy=False)
    validity = fields.Integer(string='Validity (Days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", store=True)

    _sql_constraints = [('positive_offer_price', 'check(price > 0)', 'The offer price must be strictly positive.')]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = ((rec.create_date or datetime.now()) + timedelta(days=rec.validity)).date()

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - (rec.create_date or datetime.now()).date()).days

    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                property_id = self.env['estate.property'].browse(vals.get('property_id', False))
                if property_id.offer_ids:
                    min_price = min(property_id.offer_ids.mapped('price'))
                    if float_compare(vals.get('price'), min_price, precision_rounding=0.01) <= 0:
                        raise UserError(_(f'The offer must be higher than {min_price}'))
                property_id.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        if self.property_id.offer_ids.filtered(lambda offer: offer.state == 'accepted'):
            raise UserError(_('One offer is already accepted.'))
        self.write({'state': 'accepted'})
        return self.property_id.write({'selling_price': self.price,
                                       'partner_id': self.partner_id.id,
                                       'state': 'offer_accepted'})

    def action_refuse(self):
        return self.write({'state': 'refused'})
