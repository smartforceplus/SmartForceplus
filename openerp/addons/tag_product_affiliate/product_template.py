from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class tag_affiliate_product(models.Model):

    _inherit = "product.template"
    
    affiliate = fields.Many2one('res.partner', string="Affiliate")
    affiliate_cut = fields.Float(string="Affiliate Cut (%)")