from odoo import models, fields, api
from datetime import date


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Information'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #chatter

    _rec_name = 'full_name' #so the default name doesn't leak into gui!!!!!!!


    # Patient Fields
    patient_id = fields.Char(string="Patient ID", readonly=True, copy=False, store=True, tracking=True)
    
    first_name = fields.Char(string="First Name*", required=True, store=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, store=True, tracking=True)
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", store=True, tracking=True)
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age", store=True, tracking=True)
    address = fields.Text(string="Address", store=True, tracking=True, default="İstanbul, Turkey")

    phone = fields.Char(string="Phone", store=True, tracking=True, default="+90 555 555 55 55")
    email = fields.Char(string="Email", store=True, tracking=True)
    national_id_no = fields.Char(string="National ID No", store=True, tracking=True)

    user_id = fields.Many2one('res.users', string="Related User", store=True, tracking=True, readonly=True)

    # sql constraints
    _sql_constraints = [
        ('unique_national_id', 'unique(national_id_no)', 'National ID No must be unique.')
    ]

    #email filler for demo
    @api.onchange('first_name', 'last_name')
    def _onchange_name_fields(self):
        for record in self:
            if record.first_name and record.last_name and not record.email:
                record.email = f"{record.first_name.lower()}@{record.last_name.lower()}.com"

    # generate patient id from hospital_sequence.xml
    @api.model
    def create(self, vals):

        vals['patient_id'] = self.env['ir.sequence'].next_by_code('patient.id.seq')
        return super(Patient, self).create(vals)

    # first + last name
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    # compute age
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


    @api.model
    def create(self, vals):
        patient = super().create(vals)

        if not patient.user_id and patient.email:
            group_patient = self.env.ref('odoo_medical_module.group_hospital_patient')
            group_internal = self.env.ref('base.group_user')

            user = self.env['res.users'].sudo().create({
                'name': patient.full_name,
                'login': patient.email,
                'email': patient.email,
                'password': patient.email,
                'groups_id': [(6, 0, [group_internal.id, group_patient.id])]
            })

            patient.user_id = user.id

        return patient
