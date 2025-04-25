from odoo import models, fields

class HospitalTreatment(models.Model):
    _name = 'hospital.treatment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #for chatter view!
    _description = 'Hospital Treatment'

    name = fields.Char(string="Treatment Name", required=True, tracking=True)
    is_done = fields.Boolean(string="Is Done", default=False, tracking=True)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", tracking=True)
