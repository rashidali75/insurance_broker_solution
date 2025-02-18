from odoo import fields, models


class TransactionTypeLine(models.Model):
    _name = 'transaction.type.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transaction Type Line'

    name = fields.Char(string="Name", tracking=True, help="Document Name")
    description = fields.Char(string="Description", tracking=True, help="Description")
    required = fields.Boolean(string="Active", tracking=True, help="Active", default=False)
    transaction_id = fields.Many2one(
        comodel_name='transaction.type',
        string='Transaction Type',
        help="Transaction Type",
        required=True, ondelete='cascade')
