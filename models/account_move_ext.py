from odoo import fields, models


class AccountMoveExt(models.Model):
    _inherit = "account.move"

    insurance_policy_id = fields.Many2one('insurance.policy', string="Insurance Policy", tracking=True)
    insurance_transaction_id = fields.Many2one('insurance.transaction', string="Insurance Transaction", tracking=True)
