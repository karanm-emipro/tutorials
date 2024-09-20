from email.policy import default

from odoo import api, fields, models


class Record(models.Model):
    _name = 'record.public'
    _rec_name = 'id'
    _check_company_auto = True
    _parent_name = 'parent_id'
    _parent_store = True

    info = fields.Text(string="Info", required=True)
    company_info = fields.Text(string="Company Dependent Info", company_dependent=True, required=True)
    display_info = fields.Text(string='Final Information', compute='_compute_display_info')
    company_id = fields.Many2one(comodel_name='res.company', string="Company", required=True, default=lambda self: self.env.company)
    property_id = fields.Many2one('estate.property', string="Property", check_company=True)
    parent_id = fields.Many2one('record.public', string="Parent")
    parent_path = fields.Char(string="Parent Path", index=True)
    child_ids = fields.One2many("record.public", "parent_id", string="Child Records")

    @api.depends_context('company')
    def _compute_display_info(self):
        for record in self:
            record.display_info = (record.info or '') + ' ' + (record.company_info or '')

    @api.model
    def create(self, vals):
        return super().create(vals)
