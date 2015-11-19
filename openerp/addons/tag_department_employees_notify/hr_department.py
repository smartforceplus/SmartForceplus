from openerp import models, fields, api
from datetime import datetime, timedelta
import openerp
import pytz
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)

class tag_hr_department(models.Model):

    _inherit = 'hr.department'
    
    department_tasks = fields.One2many('project.task','x_dep', string="Department Tasks")
    task_list = fields.Html(string="Task List", compute="_task_list")
    employee_ids = fields.Many2many('hr.employee', string="Employees")
    
    @api.one
    @api.depends('department_tasks', 'department_tasks.name', 'task_list')
    def _task_list(self):
        for task in self.department_tasks:
            self.task_list = str(self.task_list) + "<br/>" + str(task.name)