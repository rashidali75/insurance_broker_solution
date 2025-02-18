from odoo import fields, models, api, _


class ResPartnerExt(models.Model):
    _inherit = 'res.partner'

    is_insurer = fields.Boolean(string="Is Insurer", tracking=True)
    alias = fields.Char(string='Alias', help="Alias", tracking=True)
    client = fields.Char(string='Client ID', readonly=True, help="we use this field to get unique sequence",
                         tracking=True)
    category = fields.Char(string='Category', help="Partner Category")
    insurance_policy_id = fields.Many2one('insurance.policy',
                                          domain="[('partner_id', '=',id)]",
                                          help='this field give insurance policy according to the current partner',
                                          tracking=True)
    insurance_transaction_id = fields.Many2one('insurance.transaction', domain="[('partner_id', '=',id)]",
                                               help='this field give transaction according to the current partner',
                                               tracking=True)
    insurance_policy_ids = fields.One2many('insurance.policy', 'partner_id', domain="[('partner_id', '=',id)]")
    insurance_transaction_ids = fields.One2many('insurance.transaction', 'partner_id',
                                                domain="[('partner_id', '=',id)]")
    compliance_line_ids = fields.One2many(
        comodel_name='compliance.line',
        inverse_name='partner_id', string="Required Document",
        help="Transaction Required Document", compute='_compute_compliance_line_ids')

    @api.depends('insurance_transaction_ids')
    def _compute_compliance_line_ids(self):
        """
        *===================================*
        * Compute All Document That are not Selected in Insurance Transaction *
        *===================================*
        """
        for record in self:
            transactions = self.env['insurance.transaction'].search([('partner_id', '=', record.id)])
            filtered_documents = transactions.mapped('transaction_document_ids').filtered(lambda doc: not doc.required)
            vals_list = [{
                'name': doc.name,
                'required': doc.required,
                'description': doc.description,
                'partner_id': transactions.partner_id.id,
            } for doc in filtered_documents]
            document_ids = self.env['compliance.line'].search([('partner_id', '=', transactions.partner_id.id)])
            document_ids.unlink()
            record.compliance_line_ids.create(vals_list)

    @api.model_create_multi
    def create(self, vals_list):
        """
        *===================================*
        * get sequence number when record is generated *
        *===================================*
        """
        for vals in vals_list:
            if not vals.get('client') or vals['client'] == _('New'):
                vals['client'] = self.env['ir.sequence'].next_by_code('insurance_broker_solution.client') or _(
                    'New')
        return super(ResPartnerExt, self).create(vals_list)

    def copy(self, default=None):
        """
        *===================================*
        * get unique sequence number when record is duplicated *
        *===================================*
        """
        default = dict(default or {})
        default['client'] = self.env['ir.sequence'].next_by_code('insurance_broker_solution.client') or _('New')
        return super(ResPartnerExt, self).copy(default)
