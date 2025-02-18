from odoo import fields, models, api
import logging

logger = logging.getLogger(__name__)


class PolicyCommissionLine(models.Model):
    _name = 'policy.commission.line'
    _description = 'Policy Commission Line'

    risk_type_id = fields.Many2one('risk.type', string="Risk Type", help="Type of risk associated.")
    sr_no = fields.Char(string="Index No.", help="Index No.")
    insurer_id = fields.Many2one('res.partner', domain=[('is_insurer', '=', True)], ondelete='cascade')
    ppn = fields.Char(string="PPN", help="Policy or identification number.")
    police_number = fields.Char(string="Police Number", help="Police Number.")
    commission_amount = fields.Float(string="Commission %", help="Commission amount.")
    commission_line_id = fields.Many2one('insurance.policy', ondelete='cascade')

    @api.onchange('insurer_id')
    def _update_policy_line(self):
        """
        =====================================================
        *Get Risk Type id and commission Amount of Commission Log Model*
        =====================================================
        """
        if self.insurer_id:
            commission_log = self.env['commission.log'].search(
                [('insurer_id', '=', self.insurer_id.id), ('risk_type_id', '=', self.commission_line_id.risk_type.id)])
            self.risk_type_id = commission_log.risk_type_id.id
            self.commission_amount = commission_log.commission_amount

    def create_sequence(self, code, sequence_name):
        """
        =====================================================
        *Create the Sequence Number*
        =====================================================
        """
        sequence = {
            'name': sequence_name,
            'code': code,
            'implementation': 'standard',
            'padding': 1,
            'number_increment': 1,
            'number_next': 0,
        }
        self.env['ir.sequence'].create(sequence)

    @api.onchange('sr_no')
    def get_lines_count(self):
        """
        =====================================================
        *Update the count and SR No fields of policy commission lines based on the lead insurer and co-insurers.*
        =====================================================
        """
        for order in self:
            sequence_name = 'Insurer Details'
            code = "policy.commission.line"
            sequence_obj = self.env['ir.sequence'].search([('code', '=', code)]).ids
            policy = order.commission_line_id.policy_commission_ids[0].sr_no
            referral_sequence = self.env['ir.sequence'].browse(sequence_obj)
            if not policy:
                referral_sequence.unlink()
                order.sr_no = 'Lead Insurer 1'
            else:
                order.create_sequence(code, sequence_name)
                order.sr_no = str(f'Co-Insurer {len(referral_sequence) + 1}')
