from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class ProjectIssueVSS(models.Model):

    _inherit = "project.issue"
    
    url = fields.Char(string="Problem URL")
    ref_url = fields.Char(string="Ref URL")