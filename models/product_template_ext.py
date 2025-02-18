from odoo import fields, models


class ProductTemplateExt(models.Model):
    _inherit = 'product.template'

    gross_origin = fields.Char(string='Gross Origin', tracking=True)
