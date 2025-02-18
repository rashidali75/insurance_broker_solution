from odoo import fields, models, api, Command


class InsuranceTransaction(models.Model):
    _name = 'insurance.transaction'
    _description = 'Insurance Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(default='New', tracking=True)
    status = fields.Selection([('renewal_notice', 'Renewal Notice'),
                               ('renewal', 'Renewal'),
                               ('endorsement', 'Endorsement'),
                               ('business', 'New Business'),
                               ('cancel', 'Cancelled')],
                              default='renewal_notice', string='Transaction Type', tracking=True)

    partner_id = fields.Many2one('res.partner', string='Insured',
                                 help='Search account to relate the transaction', tracking=True)
    currency_id = fields.Many2one('res.currency', domain="[('active', '=', True)]")
    policy_number = fields.Text(string='Policy number', help='Search Policy to relate the transaction', tracking=True)

    effective_date = fields.Date(string='Effective Date',
                                 help='Start date for the current active period', tracking=True)

    transaction_details = fields.Char(string='Details',
                                      help='Auto-fill if renewal', tracking=True)

    gross_premium = fields.Integer(string='Gross Premium', tracking=True)
    taxes_ids = fields.Many2many('account.tax', column1='insurance_transaction_id', column2='account_tax_id',
                                 string='Taxes', tracking=True)
    additional_premium = fields.Float(string='Additional Premium', tracking=True)
    total_premium = fields.Float(string='Total Premium', tracking=True, compute='_calculate_total_premium')
    slip_sent = fields.Selection([('yes', 'Yes'),
                                  ('no', 'No'),
                                  ('na', 'Na')],
                                 default='na',
                                 string='Slip Send',
                                 help='Broker Slip sent', tracking=True)
    slip_received = fields.Selection([('yes', 'Yes'),
                                      ('no', 'No'),
                                      ('na', 'Na')],
                                     default='na',
                                     string='Slip Received',
                                     help='Signed Broker Slip Received', tracking=True)
    schedule_received = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No'),
                                          ('na', 'Na')],
                                         default='na',
                                         string='schedule Received',
                                         help='Schedule Received', tracking=True)
    invoice_sent = fields.Selection([('yes', 'Yes'),
                                     ('no', 'No'),
                                     ('na', 'Na')],
                                    default='na',
                                    string='Invoice Sent',
                                    help='Invoice Sent', tracking=True)
    payment_method = fields.Selection([('bank', 'Bank'),
                                       ('cash', 'Cash'),
                                       ('direct_deposit', 'Direct Deposit'),
                                       ('direct_insurer', 'Direct Insurer'),
                                       ('payment_terms', 'Payment Terms'),
                                       ('premium_finance', 'Premium Financing'),
                                       ('other', 'Other')],
                                      string='Invoice Sent',
                                      help='Invoice Sent', tracking=True)
    payment_notes = fields.Char(string='Payment Notes', tracking=True)
    premium_status = fields.Integer(string='Premium Status', tracking=True)
    outstanding_premium = fields.Integer(string='Total Outstanding Premium', tracking=True)
    payment_received = fields.Integer(string='Total Payment Received', tracking=True)
    underwriting_status = fields.Selection([('pending', 'pending'),
                                            ('insurer', 'Sent to insurer'),
                                            ('abandoned', 'Abandoned')],
                                           string='Underwriting Status',
                                           help='Underwriting Status', tracking=True)
    comments = fields.Text(string='Underwriting Comments', tracking=True)
    slip_sent_date = fields.Date(string='Date Broker Slip Sent', tracking=True)
    slip_signed_date = fields.Date(string='Slip Signed Date',
                                   help='Date Signed Broker Slip Received', tracking=True)
    received_date = fields.Date(string='Received Date',
                                help='Date Schedule Received', tracking=True)
    invoice_sent_date = fields.Date(string='Invoice Sent Date',
                                    help='Invoice Sent Date', tracking=True)
    delivery_method = fields.Selection([('standard', 'Standard'),
                                        ('h_delivery', 'Hand Delivery'),
                                        ('nearest_insurer', 'Nearset Insurer'),
                                        ('broker_office', 'Broker Office'),
                                        ],
                                       string='Delivery Method', tracking=True)
    delivery_notes = fields.Text(string='Delivery Notes', tracking=True)
    insurance_policy_id = fields.Many2one('insurance.policy', string='Insurance Policy', tracking=True)
    invoice_ids = fields.Many2many('account.move', compute="_compute_invoice_counts", string='Invoice', copy=False,
                                   store=True)
    invoice_count = fields.Integer(compute="_compute_invoice_counts", string='Invoice Count', copy=False, default=0,
                                   store=True)
    transaction_document_ids = fields.One2many(
        comodel_name='transaction.document',
        inverse_name='insurance_transaction_id',
        string="Required Document",
        help="Transaction Required Document")

    @api.onchange('status')
    def fetch_transaction_type_lines(self):
        """
        =====================================================
        * Get All required Documents Whose status is Same *
        =====================================================
        This method is triggered when the 'status' field changes.
        It fetches transaction type lines that have the same status
        as the current record and updates the 'transaction_document_ids' field.
        """
        for record in self:
            if record.status:
                # Search for transaction type lines with the same status as the current record
                transaction_type_lines = self.env['transaction.type.line'].search(
                    [('transaction_id.status', '=', record.status)]
                )

                # Prepare a list to hold the new lines' values
                line_vals = []
                for line in transaction_type_lines:
                    line_vals.append((0, 0, {
                        'name': line.name,
                        'partner_id': record.partner_id.id
                    }))

                # Mark the existing lines for deletion
                for prev_line in self.transaction_document_ids:
                    line_vals.append((3, prev_line.id, 0))

                # Write the new list of transaction document lines to the record
                record.write({
                    'transaction_document_ids': line_vals,
                })

    def _compute_invoice_counts(self):
        """
        =====================================================
        *Compute All the Invoice Ids and Also Count the Length*
        =====================================================
        """

        for order in self:
            invoice_ids = self.env['account.move'].search(
                [('invoice_origin', '=', order.name), ('insurance_policy_id', '=', order.insurance_policy_id.id),
                 ('insurance_transaction_id', '=', order.id)])
            if invoice_ids:
                order.invoice_ids = invoice_ids
                order.invoice_count = len(invoice_ids)

    @api.depends('gross_premium', 'taxes_ids', 'additional_premium')
    def _calculate_total_premium(self):
        """
        =====================================================
        *Calculate the Total Premium*
        =====================================================
        """

        for rec in self:
            total_tax = sum(rec.gross_premium * tax.amount / 100 for tax in rec.taxes_ids) or 0
            rec.total_premium = rec.gross_premium + total_tax + rec.additional_premium

    def action_view_invoice(self, invoices=False):
        """
        =====================================================
        *This function returns an action that display existing vendor bills of
        given purchase order ids. When only one found, show the vendor bill
        immediately.*
        =====================================================
        """
        if not invoices:
            self.invalidate_model(['invoice_ids'])
            invoices = self.invoice_ids
        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    @api.model
    def create(self, vals):
        """
        =====================================================
        *Create the New Record Of Insurance Transaction*
        =====================================================
        """
        vals['name'] = self.env['ir.sequence'].next_by_code('insurance.transaction') or 'New'
        if vals.get('status') == 'cancel':
            if vals.get('policy_id'):
                policy_id = self.env['insurance.policy'].browse(vals['insurance_policy_id'])
                policy_id.update({'status': 'cancel'})
        result = super(InsuranceTransaction, self).create(vals)
        return result

    def write(self, data):
        """
        =====================================================
        *Update the Existing Record Of Insurance Transaction*
        =====================================================
        """
        res = super(InsuranceTransaction, self).write(data)
        if self.status == 'cancel' and self.insurance_policy_id:
            self.insurance_policy_id.status = 'cancel'
        return res

    def transaction_endorsement(self):
        self.status = 'endorsement'

    def transaction_business(self):
        self.status = 'business'

    def create_transaction_invoice(self):
        """
        =====================================================
        * Creates an invoice for the related insurance transaction *
        =====================================================
        """
        gross_product = self.env.ref('insurance_broker_solution.gross_premium_custom_product')
        additional_product = self.env.ref('insurance_broker_solution.additional_premium_custom_product')
        product_account_income_id = gross_product.categ_id.property_account_income_categ_id.id
        journal = self.env['account.journal'].search(
            [('type', '=', 'sale'), ('company_id', '=', self.env.company.id)])
        invoice_lines = [
            {
                'product_id': gross_product.product_variant_id.id,
                'quantity': 1,
                'price_unit': self.gross_premium,
                'name': gross_product.name,
                'tax_ids': Command.set(self.taxes_ids)[2],
                'account_id': product_account_income_id,
            },
            {
                'product_id': additional_product.product_variant_id.id,
                'quantity': 1,
                'price_unit': self.additional_premium,
                'name': additional_product.name,
                'tax_ids': [],
                'account_id': product_account_income_id,
            }
        ]
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': journal.id,
            'insurance_policy_id': self.insurance_policy_id.id if self.insurance_policy_id else False,
            'insurance_transaction_id': self.id if self else False,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.company.id,
            'currency_id': self.currency_id.id if self.currency_id else self.env.company.currency_id.id,
            'invoice_line_ids': [(fields.Command.create(line)) for line in invoice_lines]
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self._compute_invoice_counts()

    def copy(self, default=None):
        """
        =====================================================
        * Duplicate Record and Change the Status to renewal_notice*
        =====================================================
        """
        res = super(InsuranceTransaction, self).copy(default=default)
        for rec in res:
            rec.status = 'renewal_notice'
        return res

    """
       *=========================================*
       * View Partner Insurance Transaction Form *
       *=========================================*
    """

    def view_insurance_transaction(self):
        """
            return:Current Insurance Transaction Form View
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transaction Partner',
            'res_model': 'insurance.transaction',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
