from odoo import fields, models, api
from ..tools.validation_duplicate_records import validation_on_duplicate_records


class PolicyExtension(models.Model):
    _name = 'policy.extension'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Policy Extension'
    _rec_name = 'risk_type_id'

    risk_type_id = fields.Many2one('risk.type', string="Risk Type", help="Type of risk associated.", tracking=True,
                                   ondelete='cascade')
    risk_description = fields.Text(string='Description', tracking=True,
                                   help="Description of the Risk type")

    @api.constrains('risk_type_id')
    def _check_unique_value(self):
        """
        =====================================================
        *Make Unique Entry*
        =====================================================
        """
        validation_on_duplicate_records(self=self, risk_type='risk_type_id', insurer_field=False)
