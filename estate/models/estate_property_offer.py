from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (Days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

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

    def action_refuse(self):
        self.state = 'refused'
