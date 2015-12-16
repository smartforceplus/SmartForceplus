from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class res_partner_esms(models.Model):

    _inherit = "res.partner"

    sms_opt_out = fields.Boolean(string="SMS Opt Out", help="If true the partner can't be sent mass sms, regular sms is stil fine though")    
    mobile_e164 = fields.Char(string="Mobile e164", store=True, compute='_calc_e164')

    @api.one
    @api.depends('country_id','mobile')
    def _calc_e164(self):
        if self.mobile and self.country_id and self.country_id.mobile_prefix:
            
            temp_e164 = ""
            if self.mobile.startswith("0"):
                temp_e164 = self.country_id.mobile_prefix + self.mobile[1:]
            elif self.mobile.startswith("+"):
                temp_e164 = self.mobile
            else:
                temp_e164 = self.country_id.mobile_prefix + self.mobile
            
            self.mobile_e164 = temp_e164.replace(" ","")
            
        else:
            self.mobile_e164 = self.mobile