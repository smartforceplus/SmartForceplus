from openerp import models, fields, api
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class html_gen_tran(models.TransientModel):

    _name = "html.trans"
    
    name = fields.Char(string='Form Name', required='True')
    campaign_id = fields.Many2one('marketing.campaign', required='True', string='Campaign')

    @api.one
    def setup_form(self):
    
        #get the id of crm.lead model
        crm_id = self.env['ir.model'].search([('model', '=', 'crm.lead')])
        
        #create tag
        my_tag_id = self.env['crm.case.categ'].create({'name': 'Campaign Tag (' + self.campaign_id.name + ')','object_id':crm_id[0].id})
        
        #create filter
        domain_string = "[['categ_ids', 'ilike', '" + my_tag_id.name + "']]"
        my_filter_id = self.env['ir.filters'].create({'name': self.campaign_id.name + ' Campaign Filter','object_id':crm_id[0].id,'model_id':'crm.lead','domain':domain_string})
        
        #create segment
        new_seg = self.env['marketing.campaign.segment'].create({'name': self.campaign_id.name,'campaign_id':self.campaign_id.id,'sync_mode':'create_date','ir_filter_id':my_filter_id.id})
        new_seg.state_running_set()
        
        #create form
        new_form_id = self.env['html.formgen'].create({'name': self.name,'campaign_id':self.campaign_id.id,'tag_id':my_tag_id.id})
        
        #get the id of contact_name and email_from        
        contact_name = self.env['ir.model.fields'].search([('name', '=', 'contact_name'),('model_id.model', '=', 'crm.lead')])
        email_from = self.env['ir.model.fields'].search([('name', '=', 'email_from'),('model_id.model', '=', 'crm.lead')])
        
        #insert contact_name and email_from as fields
        self._cr.execute('INSERT INTO html_formgen_ir_model_fields_rel VALUES(%s,%s)',(new_form_id.id,contact_name.id,))
        self._cr.execute('INSERT INTO html_formgen_ir_model_fields_rel VALUES(%s,%s)',(new_form_id.id,email_from.id,))
        #new_form_id._generate_form()

class html_gen(models.Model):

    _name = "html.formgen"

    name = fields.Char(string='Form Name', required='True', readonly=True)
    campaign_id = fields.Many2one('marketing.campaign', required='True', string='Campaign', readonly=True)
    fields_ids = fields.Many2many('ir.model.fields', domain="['|',('ttype','=','char'),'|',('ttype','=','text'),('ttype','=','integer'),('name','!=','create_date'),('name','!=','create_uid'),('name','!=','id'),('name','!=','write_date'),('name','!=','write_uid'),('model_id.model','=','crm.lead')]",string="Form Fields")
    output_html = fields.Text(string='Embed Code')
    tag_id = fields.Many2one('crm.case.categ', readonly=True)
    
    @api.one
    def generate_form(self):
        html_output = ""
        html_output += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>' + "\n"
	html_output += "<script>\n"
	html_output += "$(document).ready(function() {\n"
        html_output += '    $("#mybutton").click(function(){' + "\n"
	html_output += '        $.ajax({url:"' + request.httprequest.host_url + 'form/myinsert",dataType:"jsonp",jsonpCallback: "thanks",' + "\n"
	html_output += "        data: {\n"
	for ff in self.fields_ids:
            html_output += "            '" + ff.name + "':$('input[name=" + ff.name + "]').val(),\n"
	
	html_output += "            'form_id':" + str(self.id) + "\n"
	html_output += "        }});\n"
	html_output += "    });\n"
	html_output += '   $("#contact_form #contact_results").hide()' + "\n"
	html_output += "});\n"
	html_output += "\n"
	html_output += "function thanks(data) {\n"
	html_output += '    $("#contact_form #contact_body").slideUp();' + "\n"
	html_output += '    $("#contact_form #contact_results").hide().slideDown();' + "\n"
	html_output += "};\n"
	html_output += "</script>\n"
	html_output += '<div class="form-style" id="contact_form">' + "\n"
	html_output += "<h1>Please Contact Us</h1>\n"
	html_output += '<div id="contact_results">' + "\n"
	html_output += "Thank You for submitting the Form\n"
	html_output += "</div>\n"
	html_output += '<div id="contact_body">' + "\n"
        for ff in self.fields_ids:
            html_output += '<b>' + ff.field_description
            
            if ff.required == True:
                html_output += ' *'
            
            html_output += '</b><br/>\n'
            
            if ff.ttype == "char":
                html_output += '<input type="text" name="' + ff.name + '"'
                
                if ff.size > 0:
                    html_output += ' maxlength="' + ff.size + '"'
                
                if ff.required == True:
                    html_output += ' required'
            
                html_output += '/><br>\n'
                
            if ff.ttype == "text":
                html_output += '<textarea name="' + ff.name + '"'
               
                if ff.required == True:
	            html_output += ' required'
	                
	        html_output += '></textarea><br>\n'
	    if ff.ttype == "integer":
                html_output += '<input type="number" name="' + ff.name + '"'
               
                if ff.required == True:
	            html_output += ' required'
	                
	        html_output += '/><br>\n'
        html_output += '<input type="button" id="mybutton" value="Submit Form"/>\n'
        html_output += "</div>\n"
        html_output += "</div>"
        self.output_html = html_output
        
        