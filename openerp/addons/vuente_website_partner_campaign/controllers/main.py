import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json
import time

class MyController(http.Controller):

    @http.route('/vwpc/signup', type="http", auth="public", website=True)
    def vwpc_signup(self, **kw):
        campaigns = request.env['marketing.campaign'].search([('state','=','running')])
        return http.request.render('vuente_website_partner_campaign.vwpc_sign_up', {'camp':campaigns})
        
    @http.route('/vwpc/thankyou', type="http", auth="public", website=True)
    def vwpc_thank_you(self, **kw):
        return http.request.render('vuente_website_partner_campaign.vwpc_thank_you', {})

    @http.route('/vwpc/process', type="http", auth="public", website=True)
    def vwpc_process(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        
        existing_res_partner = request.env['res.partner'].sudo().search([('email','=',values['email'])])
	        	        
	partner_id = 0
	if len(existing_res_partner) > 0:
	    partner_id = existing_res_partner[0].id
	else:
	    #Create the customer
	    res_partner = request.env['res.partner'].sudo().create({'name':values['name'], 'TF10': values['TF10'],'email':values['email'],'mobile':values['mobile'], 'category_id':values['campaign']})
	    partner_id = res_partner.id
	                
        
	campaign = request.env['marketing.campaign'].sudo().browse(int(values['campaign']))
	action_date = time.strftime('%Y-%m-%d %H:%M:%S')
	
	for activity in campaign.activity_ids:
	    if activity.start == True:
	        #create the workitem
	        request.env['marketing.campaign.workitem'].sudo().create( {'partner_id': partner_id, 'date': action_date, 'state': 'todo', 'res_id': partner_id, 'activity_id': activity.id} )
	
	#run the workitem(s)
	request.env['marketing.campaign.workitem'].sudo().process_all(campaign.id)
        
        #Send email now
        request.env['mail.mail'].sudo().process_email_queue()
        
        return werkzeug.utils.redirect("/vwpc/thankyou")