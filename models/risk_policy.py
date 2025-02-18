from odoo import fields, models, api


class RiskPolicy(models.Model):
    _name = 'risk.policy'
    _description = 'Risk Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'risk_type_id'

    risk_type_id = fields.Many2one('risk.type', string='Risk Type', tracking=True)
    type = fields.Selection(related='risk_type_id.type', string="Type", tracking=True, help='Stored the risk type for the visibility of the Risk policy form.')
    registration_number = fields.Char(string="Registration Number", tracking=True,
                                      help="Unique registration number of the vehicle.")
    manufacture_year = fields.Date(help="Year the vehicle was manufactured.")
    years_manufacture_id = fields.Many2one('vehicle.year', string="Manufacture Year", tracking=True,
                                           help='Year the vehicle was manufactured.')
    brand_id = fields.Many2one('fleet.vehicle.model.brand', string="Make", tracking=True,
                               help="Manufacturer or brand of the vehicle.")
    model_brand_name = fields.Char(string='Make', help='Name Manufacturer or brand of the vehicle.')
    model_id = fields.Many2one('fleet.vehicle.model', string="Model", tracking=True, help="Model of the vehicle.",
                               domain="[('vehicle_year_id', '=', years_manufacture_id)]")
    chassis_number = fields.Char(string="Chassis Number", tracking=True,
                                 help="Unique identifier for the vehicle's chassis.")
    engine_number = fields.Char(string="Engine Number", tracking=True,
                                help="Unique identifier for the vehicle's engine.")
    seating_number = fields.Integer(string="Seating Capacity", tracking=True, help="Number of seats in the vehicle.")
    cc_rating = fields.Integer(string="C.C.Rating", tracking=True,
                               help="Cubic Capacity rating of the vehicle's engine.")
    hp_rating = fields.Integer(string="H.P.Rating", tracking=True, help="Horsepower rating of the vehicle's engine.")
    hand_drive = fields.Selection(selection=[('left', 'Left Hand Drive'), ('right', 'Right Hand Drive')],
                                  string="Hand Drive", tracking=True,
                                  help="Whether the vehicle is left or right-hand drive.")
    tare_weight = fields.Integer(string="Tare Weight", tracking=True, help="Weight of the vehicle without any load.")
    lease = fields.Char(string='Interested Party/Mortgages/Lease', tracking=True,
                        help="Details of any interested party, mortgage, or lease.")
    driver_id = fields.Many2one(comodel_name='res.partner', string="Named Drivers", tracking=True,
                                help="Names of the drivers authorized to drive the vehicle.")
    sum_insured = fields.Integer(string="Sum Insured", tracking=True, help="Total insured amount for the vehicle.")
    windscreen = fields.Integer(string="Windscreen", tracking=True, help="Insured amount for the windscreen.")
    subject_matter = fields.Char(string="Subject Matter", tracking=True, help="Description or type of the vehicle.")
    subject_matter_wording = fields.Char(string="Subject Matter wording", tracking=True,
                                         help="Specific wording for the subject matter.")
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    policy_number = fields.Text(string='Policy number', tracking=True)
    origin = fields.Char(string="Reference", tracking=True)
    special_notes = fields.Text('Special Notes', help="only visible when type is motor")

    @api.onchange('type')
    def _update_fields(self):
        """
        *===================================*
        * Update the Selective Field Condition Wise *
        *===================================*
        """
        if self.type == 'motor':
            self.subject_matter = ''
            self.subject_matter_wording = ''
        elif self.type == 'property':
            self.registration_number = 0
            self.manufacture_year = False
            self.brand_id = ''
            self.model_id = ''
            self.chassis_number = ''
            self.engine_number = ''
            self.seating_number = 0
            self.cc_rating = 0
            self.hp_rating = 0
            self.hand_drive = False
            self.tare_weight = 0
            self.lease = ''
            self.driver_id = ''
            self.windscreen = 0

    @api.model
    def create(self, vals):
        """
        =====================================================
        *Creates a new risk policy record and creates a corresponding risk history record if the create_history context is set*
        =====================================================
        """
        record = super(RiskPolicy, self).create(vals)
        if self.env.context.get('create_history'):
            self.env['risk.history'].create({
                'origin': record.origin,
                'partner_id': record.partner_id.id,
                'policy_number': record.policy_number,
                'risk_type_id': record.id,
                'insurance_policy_id': self.env.context.get('default_insurance_policy_id'),
            })
        return record

    @api.onchange('model_id')
    def get_model_brands(self):
        vehicle_brand_id = self.env['fleet.vehicle.model.brand'].search([('id', '=', self.model_id.brand_id.id)])
        if vehicle_brand_id:
            self.update({
                'model_brand_name': vehicle_brand_id.name
            })
        else:
            False
