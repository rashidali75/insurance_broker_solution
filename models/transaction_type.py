from odoo import fields, models, api
from ..tools.validation_duplicate_records import validation_on_duplicate_records


class TransactionType(models.Model):
    _name = 'transaction.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transaction Type'
    _rec_name = 'status'

    status = fields.Selection([('renewal_notice', 'Renewal Notice'),
                               ('renewal', 'Renewal'),
                               ('endorsement', 'Endorsement'),
                               ('business', 'New Business'),
                               ('cancel', 'Cancelled')],
                              default='renewal_notice', string='Transaction Type', tracking=True)
    transaction_line_ids = fields.One2many(
        comodel_name='transaction.type.line',
        inverse_name='transaction_id',
        string="Transaction Line",
        help="No. of Transaction Line")

    @api.constrains('status')
    def check_unique_status(self):
        """
        =====================================================
        *Make Unique Entry*
        =====================================================
        """
        validation_on_duplicate_records(self=self, risk_type='status', insurer_field=False)
