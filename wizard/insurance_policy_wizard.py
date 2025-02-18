from odoo import fields, models, api, _


class InsurancePolicyWizard(models.TransientModel):
    _name = 'insurance.policy.wizard'
    _description = 'Insurance Policy Wizard'

    reason_note = fields.Text('Reason Note')
    policy_id = fields.Many2one('insurance.policy', 'Insurance Policy')

    def action_confirm_canel(self):
        """
        =====================================================
        *Reason Note on Cancel Record*
        =====================================================
        """
        for rec in self:
            if rec:
                rec.policy_id.reason_note = rec.reason_note
                rec.policy_id.status = 'cancel'
