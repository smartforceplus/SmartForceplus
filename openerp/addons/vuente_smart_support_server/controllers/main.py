import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json

class MyController(http.Controller):

        
    @http.route('/vss/thankyou', type="http", auth="public", website=True)
    def vss_thank_you(self, **kw):
        return http.request.render('vuente_smart_support_server.vss_thank_you', {})

    @http.route('/vss/process', type="http", auth="public", website=True)
    def vss_process(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        ref_url = http.request.httprequest.headers['Referer']

        #Create project issue
        project_issue = request.env['project.issue'].create({'name':values['name'] + " (Issue)", 'email_from': values['email'], 'url': values['url'], 'ref_url': ref_url, 'description': values['comment']})
        
                
        return werkzeug.utils.redirect("/vss/thankyou")