from odoo import fields, models, api


class RiskHistory(models.Model):
    _name = 'risk.history'
    _description = 'Risk History'
    _rec_name = 'risk_type_id'

    partner_id = fields.Many2one('res.partner', string='Customer', help='Partner', ondelete='cascade')
    policy_number = fields.Text(string='Policy number', help='Policy Number')
    risk_type_id = fields.Many2one('risk.policy', help='risk_type_id', ondelete='cascade')
    insurance_policy_id = fields.Many2one('insurance.policy', string='Insurance Policy', ondelete='cascade')
    origin = fields.Char(string="Reference")

    def view_risk_policy(self):
        """
        =====================================================
        *Opens the related risk policy form in a new window *
        =====================================================
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'risk.policy',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.risk_type_id.id,
        }
