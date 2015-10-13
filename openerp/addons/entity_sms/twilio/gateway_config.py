from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime
from lxml import etree
from openerp.http import request
from openerp.osv import osv

class sms_response():
     delivary_state = ""
     response_string = ""
     human_read_error = ""

class twilio_core(models.Model):

    _name = "esms.twilio"
    
    api_url = fields.Char(string='API URL')
    
    def send_message(self, sms_gateway_id, from_number, to_number, sms_content, my_model_name='', my_record_id=0, my_field_name=''):
        sms_account = self.env['esms.accounts'].search([('id','=',sms_gateway_id)])
        
        #format the from number before sending
        format_from = from_number
        if " " in format_from: format_from.replace(" ", "")
        
        #format the to number before sending
        format_to = to_number
        if " " in format_to: format_to.replace(" ", "")        
        
        #send the sms/mms
        base_url = self.env['ir.config_parameter'].search([('key','=','web.base.url')])[0].value
        payload = {'From': str(format_from), 'To': str(format_to), 'Body': str(sms_content), 'StatusCallback': base_url + "/sms/twilio/receipt"}
        response_string = requests.post("https://api.twilio.com/2010-04-01/Accounts/" + str(sms_account.twilio_account_sid) + "/Messages", data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))

        #Analyse the reponse string and determine if it sent successfully other wise return a human readable error message   
        human_read_error = ""
        root = etree.fromstring(str(response_string.text))
        my_elements_human = root.xpath('/TwilioResponse/RestException/Message')
        if len(my_elements_human) != 0:
	    human_read_error = my_elements_human[0].text
        
        #The message id is important for delivary reports also set delivary_state=successful
	sms_gateway_message_id = ""
	delivary_state = "failed"
	my_elements = root.xpath('//Sid')
	if len(my_elements) != 0:
	    sms_gateway_message_id = my_elements[0].text
            delivary_state = "successful"
        
        #only record the sent sms/mms if it was successfully sent, multi send sms records it inconsiderate
        if delivary_state == "successful":
            my_model = self.env['ir.model'].search([('model','=',my_model_name)])
	    my_field = self.env['ir.model.fields'].search([('name','=',my_field_name)])
            esms_history = self.env['esms.history'].create({'field_id':my_field[0].id, 'record_id': my_record_id,'model_id':my_model[0].id,'account_id':sms_account.id,'from_mobile':format_from,'to_mobile':to_number,'sms_content':sms_content,'status_string':response_string.text, 'direction':'O','my_date':datetime.utcnow(), 'status_code':delivary_state, 'sms_gateway_message_id':sms_gateway_message_id, 'gateway_id': sms_account.account_gateway.id})
        
        #send a repsonse back saying how the sending went
        my_sms_response = sms_response()
        my_sms_response.delivary_state = delivary_state
        my_sms_response.response_string = response_string.text
        my_sms_response.human_read_error = human_read_error
        return my_sms_response

    def check_messages(self, account_id, message_id=""):
        _logger.error("check")
        sms_account = self.env['esms.accounts'].browse(account_id)
        
        if message_id != "":
            response_string = requests.get("https://api.twilio.com/2010-04-01/Accounts/" + sms_account.twilio_account_sid + "/Messages/" + message_id, data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))
	    root = etree.fromstring(str(response_string.text))
	    my_messages = root.xpath('//Message')
            sms_message = my_messages[0]
            #only get the inbound ones as we track the outbound ones back to a user profile
            if sms_message.xpath('//Direction')[0].text == "inbound":
                self._add_message(sms_message, account_id)        
        else:
            #get a list of all new inbound message since the last check date
            payload = {}
            if sms_account.twilio_last_check_date != False:
                my_time = datetime.strptime(sms_account.twilio_last_check_date,'%Y-%m-%d %H:%M:%S')
                payload = {'DateSent>': str(my_time.strftime('%Y-%m-%d'))}
            response_string = requests.get("https://api.twilio.com/2010-04-01/Accounts/" + sms_account.twilio_account_sid + "/Messages", data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))
            root = etree.fromstring(str(response_string.text))
            
            
            #get all pages
            messages_tag = root.xpath('//Messages')
            
            
            num_pages = messages_tag[0].attrib['numpages']
            for sms_page in xrange(0, int(num_pages)):
                my_messages = messages_tag[0].xpath('//Message')
                for sms_message in my_messages:
                    
                    #only get the inbound ones as we track the outbound ones back to a user profile
                    if sms_message.find('Direction').text == "inbound":
                        self._add_message(sms_message, account_id)
                        
                #get the next page if there is one
                if sms_page < (int(num_pages) - 1):
                    response_string = requests.get("https://api.twilio.com" + messages_tag[0].attrib['nextpageuri'], data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))
		    root = etree.fromstring(str(response_string.text))
		    messages_tag = root.xpath('//Messages')
		
	
        sms_account.twilio_last_check_date = datetime.utcnow()
            
    def _add_message(self, sms_message, account_id):
                        
        delivary_state = ""
	if sms_message.find('Status').text == "failed":
	    delivary_state = "failed"
        elif sms_message.find('Status').text == "sent":
	    delivary_state = "successful"
	elif sms_message.find('Status').text == "delivered":
	    delivary_state = "DELIVRD"
	elif sms_message.find('Status').text == "undelivered":
	    delivary_state = "UNDELIV"
	elif sms_message.find('Status').text == "received":
	    delivary_state = "RECEIVED"
	
        my_message = self.env['esms.history'].search([('sms_gateway_message_id','=', sms_message.find('Sid').text)])
        if len(my_message) == 0 and sms_message.find('Direction').text == "inbound":
            #look for a partner with this number
            partner_id = self.env['res.partner'].search([('mobile','=', sms_message.find('From').text)])
	    if len(partner_id) > 0:
	        record_id = partner_id[0]
	    	target_model = "res.partner"
	    	target_field = "mobile"
	    else:
	        #If you can't find a partner with that mobile number then look for a lead with that number
	    	lead_id = self.env['crm.lead'].search([('mobile','=', sms_message.find('From').text)])
	    	if len(lead_id) > 0:
	    	    record_id = lead_id[0]
	    	    target_model = "crm.lead"
	    	    target_field = "mobile"
	        else:
	            #can't find the record so create a new lead
	            target_model = "crm.lead"
	    	    target_field = "mobile"
	            record_id = self.env['crm.lead'].create({'name': 'Mobile Lead', 'mobile':sms_message.find('From').text})
	            
	    model_id = self.env['ir.model'].search([('model','=', target_model)])
	    field_id = self.env['ir.model.fields'].search([('model_id.model','=',target_model), ('name','=', target_field)])
	    twilio_gateway_id = self.env['esms.gateways'].search([('gateway_model_name', '=', 'esms.twilio')])
	            
	    #Create the sms record in history
	    history_id = self.env['esms.history'].create({'account_id': account_id, 'status_code': "RECEIVED", 'gateway_id': twilio_gateway_id[0].id, 'from_mobile': sms_message.find('From').text, 'to_mobile': sms_message.find('To').text, 'sms_gateway_message_id': sms_message.find('Sid').text, 'sms_content': sms_message.find('Body').text, 'direction':'I', 'my_date':sms_message.find('DateUpdated').text, 'model_id':model_id.id, 'record_id':record_id, 'field_id':field_id.id})
                    
    def delivary_receipt(self, account_sid, message_id):
        my_account = self.env['esms.accounts'].search([('twilio_account_sid','=', account_sid)])[0]
        response_string = requests.get("https://api.twilio.com/2010-04-01/Accounts/" + my_account.twilio_account_sid + "/Messages/" + message_id, auth=(str(my_account.twilio_account_sid), str(my_account.twilio_auth_token)))
        root = etree.fromstring(str(response_string.text))
        
        #map the Twilio delivary code to the esms delivary states 
	delivary_state = ""
	if root.xpath('//status')[0].text == "failed":
	    delivary_state = "failed"
	elif root.xpath('//status')[0].text == "sent":
	    delivary_state = "successful"
	elif root.xpath('//status')[0].text == "delivered":
	    delivary_state = "DELIVRD"
	elif root.xpath('//status')[0].text == "undelivered":
	    delivary_state = "UNDELIV"
        
        my_message = self.env['esms.history'].search(['sms_gateway_message_id','=', message_id])
        if len(my_message) > 0:
            self.status_code = delivary_state
            self.delivary_error_string = root.xpath('//ErrorMessage')[0].text        
            
class twilio_conf(models.Model):

    _inherit = "esms.accounts"
    
    twilio_account_sid = fields.Char(string='Account SID')
    twilio_auth_token = fields.Char(string='Auth Token')
    twilio_last_check_date = fields.Datetime(string="Last Check Date")
    
    @api.one
    def twilio_quick_setup(self):
	response_string = requests.get("https://api.twilio.com/2010-04-01/Accounts/" + self.twilio_account_sid, auth=(str(self.twilio_account_sid), str(self.twilio_auth_token)))
        if response_string.status_code == 200:
            response_string_twilio_numbers = requests.get("https://api.twilio.com/2010-04-01/Accounts/" + self.twilio_account_sid + "/IncomingPhoneNumbers", auth=(str(self.twilio_account_sid), str(self.twilio_auth_token)))
            
            #go through each twilio number in the account and set the the sms url
            root = etree.fromstring(str(response_string_twilio_numbers.text))
	    my_from_number_list = root.xpath('//IncomingPhoneNumber')
	    for my_from_number in my_from_number_list:
	        sid = my_from_number.xpath('//Sid')[0].text
	        
	        payload = {'SmsUrl': str(request.httprequest.host_url + "sms/twilio/receive")}
	        requests.post("https://api.twilio.com/2010-04-01/Accounts/" + self.twilio_account_sid + "/IncomingPhoneNumbers/" + sid, data=payload, auth=(str(self.twilio_account_sid), str(self.twilio_auth_token)))
                
	    raise osv.except_osv(("Setup Successful"), ("All Done"))
        else:
            raise osv.except_osv(("Setup Failed"), ("Bad Credentials"))

