from odoo import fields, models, api
from ..tools.validation_duplicate_records import validation_on_duplicate_records


class RiskType(models.Model):
    _name = 'risk.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Risk Type'
    _rec_name = 'name'

    name = fields.Char('Title', compute='_compute_display_name',
                       help='Compute the display name of the risk type', tracking=True)
    type = fields.Selection(selection=[('motor', 'Motor'), ('property', 'Property')],
                            string="Risk Type", tracking=True,
                            help="Unique registration number of the vehicle.")
    risk_description = fields.Text(string='Description', tracking=True,
                                   help="Description of the Risk type")

    @api.depends('name')
    def _compute_display_name(self):
        """
        *===================================*
        * Displays the Customised _rec_name *
        *===================================*
        """
        for rec in self:
            rec.display_name = "%s - %s" % (rec.risk_description, rec.type)

    @api.constrains('type')
    def _check_unique_value(self):
        """
        =====================================================
        *Make Unique Entry*
        =====================================================
        """
        validation_on_duplicate_records(self=self, risk_type='type', insurer_field=False)
