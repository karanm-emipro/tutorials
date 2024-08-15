from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'sequence, name'

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offers Count', compute='_compute_offers_count')

    _sql_constraints = [('unique_property_type', 'unique(name)', 'Property house must be unique.')]

    def _compute_offers_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_show_offers(self):
        action = self.env['ir.actions.act_window']._for_xml_id('estate.estate_property_offer_action')
        action['domain'] = [('property_type_id', '=', self.id)]
        return action
