import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json

class MyController(http.Controller):

    @http.route('/vwpc/signup', type="http", auth="public", website=True)
    def vwpc_signup(self, **kw):
        campaign_tags = request.env['res.partner.category'].search([])
        return http.request.render('vuente_website_partner_campaign.vwpc_sign_up', {'camp':campaign_tags})
        
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
	    res_partner = request.env['res.partner'].sudo().create({'name':values['name'], 'TF10': values['TF10'],'email':values['email'], 'category_id':values['campaign']})
	    partner_id = res_partner.id
	                
                
        request.cr.execute('INSERT INTO res_partner_res_partner_category_rel VALUES(' + str(values['campaign']) + ',' + str(partner_id) + ')')
        
        return werkzeug.utils.redirect("/vwpc/thankyou")