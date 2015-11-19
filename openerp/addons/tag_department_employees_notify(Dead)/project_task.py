from openerp import models, fields, api
from datetime import datetime, timedelta
import openerp
import pytz
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)

class tag_project_task_email(models.Model):

    _inherit = 'project.task'
    
    x_dep = fields.Many2one('hr.department',string="Department")
 
    @api.onchange('x_dep')
    @api.depends('x_dep')
    def tag_email_department(self):
        employee_list = []
        _logger.error("1")
        email_template = self.env['ir.model.data'].get_object('tag_department_employees_notify', 'email_department')
        _logger.error(self.x_dep.id)
        #get a list of everyone in the department
        for employee in self.env['hr.employee'].search([]):
            for department in employee.x_departments:
                if department.id == self.x_dep.id:
                    employee_list.append(employee)
        
        for temp_employee in employee_list:
            employee = temp_employee
            _logger.error(employee.work_email)
	    mail_values = {}
	    #mail_values = self.env['email.template'].generate_email(email_template.id, employee.id)
	    _logger.error("et" + str(email_template.id))
	    
	    
	    mail_values['email_to'] = employee.work_email
	    mail_values['email_from'] = "stevewright2009@gmail.com"
	    mail_values['subject'] = "New Task"
	    mail_values['body_html'] = "You Have a new task for your department"
	    
	    _logger.error(mail_values['subject'])
	    _logger.error("ei" + str(employee.id))
	    _logger.error("4")
	    mail_id = self.env['mail.mail'].create(mail_values)
	    _logger.error("6")
	    self.env['mail.mail'].send(mail_id)
	    _logger.error("7")
            