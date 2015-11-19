from openerp import models, fields, api
from datetime import datetime, timedelta
import openerp
import pytz
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)

class tag_hr_employee(models.Model):

    _inherit = 'hr.employee'
    
    x_departments = fields.Many2many('hr.department',string="Department")