from odoo import models, fields


class Department(models.Model):
    _name = 'hospital.department'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #chatter
    _description = 'Hospital Department'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True, store=True, tracking=True)
    code = fields.Char(string="Code", required=True, store=True, tracking=True)
    icon = fields.Image(string="Icon", store=True, tracking=True)    

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'The department code must be unique.')
    ]
