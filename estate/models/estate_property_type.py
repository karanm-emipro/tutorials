from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    
    name = fields.Char(string="Title", required=True)

    _sql_constraints = [('unique_property_type', 'unique(name)', 'Property house must be unique.')]
