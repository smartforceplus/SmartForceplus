import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class MyController(http.Controller):

    @http.route('/form/myinsert',type="http")
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
        
    @http.route('/form/autocomplete',type="http")
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