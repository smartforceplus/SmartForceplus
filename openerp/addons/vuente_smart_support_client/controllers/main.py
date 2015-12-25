import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json

class MyController(http.Controller):

    @http.route('/vuente/support', type="http", auth="public", website=True)
    def vssc_form(self, **kw):
        ref_url = ""
        #ref_url = http.request.httprequest.headers['Referer']
        
        return http.request.render('vuente_smart_support_client.vssc_form', {'url':ref_url, 'name':http.request.env.user.partner_id.name,'email':http.request.env.user.partner_id.email})