from odoo import fields, models


class VehicleYear(models.Model):
    _name = "vehicle.year"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To Save The Record Related To Manufacturing Vehicle Year'
    _rec_name = 'year'

    year = fields.Char(string='Year', help="to save vehicle manufacturing year", tracking=True)
