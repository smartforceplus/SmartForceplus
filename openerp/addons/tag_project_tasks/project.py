from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class tag_project(models.Model):

    _inherit = "project.project"
    
    project_url = fields.Char(string='Project URL Link')

