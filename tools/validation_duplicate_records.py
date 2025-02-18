from odoo import _
from odoo.exceptions import ValidationError

"""
    ============================================================**
    * Validation When Duplicate Records In Ages Different Table **
    ============================================================**
"""


def validation_on_duplicate_records(self, risk_type, insurer_field):
    """
        :param self: Model Instance
        :param risk_type: Field Which Does Not Duplicate Records
        :param insurer_field: Field Which Does Not Duplicate Records
    """
    for rec in self:
        if risk_type == 'risk_type_id' and insurer_field == 'insurer_id':
            risk_type_field = getattr(rec, risk_type)
            insurer_field_id = getattr(rec, insurer_field)
            if self.search_count(
                    [(risk_type, '=', risk_type_field.id), (insurer_field, '=', insurer_field_id.id),
                     ('id', '!=', rec.id)]) > 0:
                raise ValidationError(_("Please Enter a Unique Insurer and Risk Type"))

        elif risk_type == 'status' and insurer_field == False:
            status_record = getattr(rec, risk_type)
            if self.search_count([(risk_type, '=', status_record), ('id', '!=', rec.id)]) > 0:
                raise ValidationError(_("Please Enter a Unique Transaction Type"))

        elif risk_type == 'type' and insurer_field == False:
            status_record = getattr(rec, risk_type)
            if self.search_count([(risk_type, '=', status_record), ('id', '!=', rec.id)]) > 0:
                raise ValidationError(_("Please Enter a Unique Type"))

        else:
            if risk_type == 'risk_type_id' and insurer_field == False:
                risk_type_record = getattr(rec, risk_type)
                if self.search_count([(risk_type, '=', risk_type_record.id), ('id', '!=', rec.id)]) > 0:
                    raise ValidationError(_("Please Enter a Unique Risk Type"))
