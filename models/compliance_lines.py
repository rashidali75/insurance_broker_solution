from odoo import fields, models


class ComplianceLines(models.Model):
    _name = 'compliance.line'
    _description = 'Compliance Lines'

    name = fields.Char(string="Name", help="Document Name")
    description = fields.Char(string="Description", help="Description")
    required = fields.Boolean(string="Active", help="Active", default=False)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 help='Search Record related to Partner')

    def view_transaction(self):
        """
        =====================================================
        *Opens the related insurance transaction form in a new window *
        =====================================================
        """
        transactions = self.env['insurance.transaction'].search([('partner_id', '=', self.partner_id.id)])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'insurance.transaction',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': transactions.id,
        }
