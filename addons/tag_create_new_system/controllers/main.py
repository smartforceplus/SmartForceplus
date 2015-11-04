import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json
import shlex, subprocess

class MyController(http.Controller):

    @http.route('/system/newinstance', type="http", auth="public", website=True)
    def tns_new_system(self, **kw):
        return http.request.render('tag_create_new_system.tns_submit_system', {})
        
    @http.route('/system/thankyou', type="http", auth="public", website=True)
    def tns_new_system_thank_you(self, **kw):
        return http.request.render('tag_create_new_system.tns_thank_you', {})

    @http.route('/tns/system/process', type="http", auth="public", website=True)
    def tnx_process(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        system_name = values['system']
        
        #remove all spaces
        system_name = system_name.replace(" ", "")
        
        #Create the customer
        res_partner = request.env['res.partner'].create({'name':values['name'] + " (System Request)", 'email':values['email'], 'comment':"Want a new system named " + system_name})
        
        #create the project and associate to the new customer
        project_project = request.env['project.project'].create({'name':system_name + " System Request",'partner_id':res_partner.id})
        
        #Add task to the new project
        project_task = request.env['project.task'].create({'name':"Create New System",'project_id':project_project.id, 'description':'Create new system(dont change its a campaign hook)'})
        
        #subprocess.Popen(["/home/tag/odoonewinstance", system_name])
        
        return werkzeug.utils.redirect("/system/thankyou")