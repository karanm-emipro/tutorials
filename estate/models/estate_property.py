from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Received'),
                              ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')],
                             string='Status', default='new', copy=False, required=True)
    description = fields.Text(string='Description', )
    postcode = fields.Char(string='Postcode', )
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: (datetime.now() + timedelta(days=90)).date())
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)', )
    facades = fields.Integer(string='Facades', )
    garage = fields.Boolean(string='Garage', )
    garden = fields.Boolean(string='Garden', )
    garden_area = fields.Integer(string='Garden Area (sqm)', )
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                           ('east', 'East'), ('west', 'West')], string='Garden Orientation', )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', reqired=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', reqired=True, copy=False)
    user_id = fields.Many2one('res.users', string='Salesman', reqired=True, default=lambda self: self._uid)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = rec.offer_ids and max(rec.offer_ids.mapped('price')) or 0

    @api.onchange('garden')
    def onchange_method(self):
        self.garden_area = self.garden and 10 or 0
        self.garden_orientation = self.garden and 'north' or False

    def action_sold(self):
        if self.state == 'cancel':
            raise UserError(_('Cancelled properties cannot be sold.'))
        self.state = 'sold'

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_('Cannot cancel sold properties.'))
        self.state = 'cancel'
