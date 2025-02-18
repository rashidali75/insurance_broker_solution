from odoo import fields, models


class FleetVehicleModelExt(models.Model):
    _inherit = 'fleet.vehicle.model'

    vehicle_year_id = fields.Many2one('vehicle.year', help='year in which vehicle model made')
