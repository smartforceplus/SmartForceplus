from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class tag_tasks(models.Model):

    _inherit = "project.task"
    _order = "create_date desc"
    
    task_url = fields.Char(string='Task URL Link')

