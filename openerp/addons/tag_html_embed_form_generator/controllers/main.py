import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)
from openerp.http import werkzeug
class MyController(http.Controller):


    @http.route('/form/tag/myinsert',type="http", auth="public")
    def my_insert(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
            
        attach_obj = request.registry['html.tag.formgen']
	rs = attach_obj.search(request.cr, SUPERUSER_ID, [('id','=',values['form_id'])],limit=1)
	rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        
        #the referral string is what the campaign looks for
        secure_values = {}
        secure_values['website'] = request.httprequest.headers['Referer']
        
        #populate an array which has ONLY the fields that are in the form (prevent injection)
        for fi in rl[0].fields_ids:
            secure_values[fi.name] = values[fi.name]

        existing_res_partner = request.env['res.partner'].search([('email','=',values['email'])])
        
        _logger.error(len(existing_res_partner))
        
        partner_id = 0
        if len(existing_res_partner) > 0:
            partner_id = existing_res_partner[0]
        else:
            #Create the customer
            new_partner = request.registry['res.partner'].create(request.cr, SUPERUSER_ID, secure_values)
            partner_id = new_partner
        
        
        _logger.error(partner_id)
        
        #Add the campaign tag
        request.cr.execute('INSERT INTO res_partner_res_partner_category_rel VALUES(' + str(rl[0].tag_id.id) + ',' + str(partner_id) + ')')
        
        #send them an email
        mail_values = request.registry['email.template'].generate_email(request.cr, SUPERUSER_ID, rl[0].template_id.id, new_lead_id)
        mail = request.registry['mail.mail'].create(request.cr, SUPERUSER_ID, mail_values)
        request.registry['mail.mail'].send(request.cr, SUPERUSER_ID, [mail])
        
        return werkzeug.utils.redirect(rl[0].thank_url,301)
    
    @http.route('/form/tag/myinsertjson',type="http")
    def some_json(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
            
        attach_obj = request.registry['html.formgen']
	rs = attach_obj.search(request.cr, SUPERUSER_ID, [('id','=',values['form_id'])],limit=1)
	rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        
        #the referral string is what the campaign looks for
        secure_values = {}
        secure_values['name'] = 'Web Lead'
        secure_values['referred'] = request.httprequest.headers['Referer']
        
        #populate an array which has ONLY the fields that are in the form (prevent injection)
        for fi in rl[0].fields_ids:
            secure_values[fi.name] = values[fi.name]
        
        new_lead_id = request.registry['crm.lead'].create(request.cr, SUPERUSER_ID, secure_values)
        
        request.cr.execute('INSERT INTO crm_lead_category_rel VALUES(' + str(new_lead_id) + ',' + str(rl[0].tag_id.id) + ')')
        
        return_string = values['callback'] + "({'mytext':'success'});"
        
        return return_string
        
    @http.route('/form/tag/autocomplete',type="http")
    def some_autocomplete(self, **kwargs):
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        _logger.error(values['q'])
        _logger.error(values['f'])
        
        return_string = ""
        attach_obj = request.registry['res.country']
        rs = attach_obj.search(request.cr, SUPERUSER_ID, [('name','=ilike',values['q'] + "%")],limit=5)
        rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        for ri in rl:
            return_string += "{'label':'" +  ri.name  + "'},"
        return_string = return_string[:-1]
        
        return_string = values['callback'] + "(" + return_string + ");"
        _logger.error(return_string)
        return return_string