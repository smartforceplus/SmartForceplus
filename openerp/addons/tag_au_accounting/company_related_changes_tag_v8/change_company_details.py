from openerp import models, fields, api

class change_company_details(models.Model):
    _inherit = 'res.company'
    
    acn_number = fields.Char(string='ACN', size=32)
    abn_number = fields.Char(string='ABN', size=32)