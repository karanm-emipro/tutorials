from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", default=_get_default_color)

    _sql_constraints = [('unique_property_tag', 'unique(name)', 'Property tag must be unique.')]
