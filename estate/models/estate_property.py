from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Estate Property"
    _order = 'id desc'

    @api.model
    def _read_group_type_ids(self, types, domain, order):
        if types.ids:
            type_ids = types._search([('id', 'in', types.ids)], order=order, access_rights_uid=SUPERUSER_ID)
        else:
            type_ids = types._search([], limit=1, order=order, access_rights_uid=SUPERUSER_ID)
        return types.browse(type_ids)

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
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', reqired=True, group_expand='_read_group_type_ids')
    partner_id = fields.Many2one('res.partner', string='Buyer', reqired=True, copy=False)
    user_id = fields.Many2one('res.users', string='Salesman', reqired=True, default=lambda self: self._uid)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('positive_expected_price', 'check(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('positive_selling_price', 'check(selling_price > 0)', 'The selling price must be strictly positive.')]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = rec.offer_ids and max(rec.offer_ids.mapped('price')) or 0

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for rec in self:
            if (rec.offer_ids.filtered(lambda offer: offer.state == 'accepted') and
                    float_compare(rec.selling_price, ((90 * rec.expected_price) / 100), precision_rounding=2) < 0):
                raise ValidationError(_('The Selling price must be at least 90% of the expected price! '
                                        'You must reduce the expected price if you want to accept this offer.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled_record(self):
        if any(rec.state not in ('new', 'cancel') for rec in self):
            raise UserError(_('Only new and cancelled properties can be deleted.'))

    @api.onchange('garden')
    def _onchange_method(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.state == 'cancel':
            raise UserError(_('Cancelled properties cannot be sold.'))
        if 'accepted' not in self.offer_ids.mapped('state'):
            raise UserError(_('No offer is accepted. Please accept a offer before selling a property.'))
        self.state = 'sold'
        self.message_post(body=f"Property sold to {self.partner_id.name}", message_type='notification')

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_('Cannot cancel sold properties.'))
        self.state = 'cancel'
        self.message_post(body="This property is no longer available for sale", message_type='notification')
