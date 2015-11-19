from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class tag_tasks(models.Model):

    _inherit = "project.task"
    _order = "create_date desc"
    
    task_url = fields.Char(string='Task URL Link')
    pri = fields.Selection((('1','A1'), ('2','A2'), ('3','B1'),('4','B2'), ('5','C1'),('6','C2'), ('7','D1'),('8','D2')),string="Priority")

