from odoo import fields, models


class TransactionDocument(models.Model):
    _name = 'transaction.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transaction Required Document'

    name = fields.Char(string="Name", tracking=True, help="Document Name")
    description = fields.Char(string="Description", tracking=True, help="Description")
    required = fields.Boolean(string="Active", tracking=True, help="Active", default=False)
    insurance_transaction_id = fields.Many2one('insurance.transaction', string='Insurance Transaction',
                                               help='Search related records of Insurance Transaction', tracking=True,
                                               ondelete='cascade')
    partner_id = fields.Many2one('res.partner', help="Partner associated with this transaction type line",
                                 tracking=True, ondelete='cascade')
