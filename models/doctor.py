from odoo import models, fields, api
from datetime import date


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # chatter
    _description = 'Doctor Information'
    _rec_name = 'full_name'

    first_name = fields.Char(string="First Name", required=True, store=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, store=True, tracking=True)
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", store=True, tracking=True)
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age", store=True, tracking=True)
    phone = fields.Char(string="Phone", store=True, tracking=True)
    email = fields.Char(string="Email", required=False, store=True, tracking=True)
    department_id = fields.Many2one('hospital.department', string="Department", store=True, tracking=True)
    shift_start = fields.Float(string="Shift Start", store=True, tracking=True)
    shift_end = fields.Float(string="Shift End", store=True, tracking=True)
    portrait = fields.Image(string="Portrait", store=True, tracking=True)

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email is already used.')
    ]

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    @api.depends('date_of_birth') #I think depends work better than onchange here??
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day)
                )
            else:
                rec.age = 0

