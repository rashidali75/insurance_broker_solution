from odoo import fields, models, api
from ..tools.validation_duplicate_records import validation_on_duplicate_records


class RiskType(models.Model):
    _name = "commission.log"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Commission Log'
    _rec_name = 'risk_type_id'

    risk_type_id = fields.Many2one('risk.type', string="Risk Type", help="Type of risk associated.", tracking=True)
    insurer_id = fields.Many2one('res.partner', domain=[('is_insurer', '=', True)], tracking=True)
    commission_amount = fields.Float(string="Commission Amount", help="Commission amount.", tracking=True)

    @api.constrains('risk_type_id', 'insurer_id')
    def check_unique_age(self):
        """
        =====================================================
        *Make Unique Entry*
        =====================================================
        """
        validation_on_duplicate_records(self=self, risk_type='risk_type_id', insurer_field='insurer_id')
