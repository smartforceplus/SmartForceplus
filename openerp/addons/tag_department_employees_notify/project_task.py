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
    
    @api.one
    def notify_dep(self):
        if self.x_dep:
            #send email out to notify everyone in that department
            notification_template = self.env['ir.model.data'].get_object_reference('tag_department_employees_notify', 'email_department')[1]        
	    for pp in self.x_dep.employee_ids:
	        values = self.env['email.template'].generate_email(notification_template, pp.id)   
	        values['email_to'] = pp.work_email
	        values['body_html'] += "<a href='http://www.smartforceplus.com/web?id=" + str(self.x_dep.id) + "&view_type=form&model=hr.department&menu_id=528&action=661'>View Department Tasks</a>" 
	        msg_id = self.env['mail.mail'].create(values)
                self.env['mail.mail'].send([msg_id], True)
        