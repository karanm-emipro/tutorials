from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


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

    _sql_constraints = [('positive_offer_price', 'check(price >= 0)', 'The offer price must be strictly positive.'),]

    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id', False))
            min_price = min(property_id.offer_ids.mapped('price') or [0])
            if min_price > vals.get('price', 0):
                raise UserError(_(f'The offer must be higher than {min_price}'))
            property_id and property_id.state == 'new' and property_id.update({'state': 'offer_received'})
        return super().create(vals_list)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = ((rec.create_date or datetime.now()) + timedelta(days=rec.validity)).date()

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - (rec.create_date or datetime.now()).date()).days

    def action_accept(self):
        if self.property_id.offer_ids.filtered(lambda offer: offer.state == 'accepted'):
            raise UserError(_('One offer is already accepted.'))
        self.state = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = 'offer_accepted'

    def action_refuse(self):
        self.state = 'refused'
