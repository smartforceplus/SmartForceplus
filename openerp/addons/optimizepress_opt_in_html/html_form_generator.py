from openerp import models, fields, api
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class html_gen_tran(models.TransientModel):

    _name = "html.trans"
    
    name = fields.Char(string='Form Name', required='True')
    campaign_id = fields.Many2one('marketing.campaign', required='True', string='Campaign')

    @api.multi
    def setup_form(self):
        self.ensure_one()
        #get the id of crm.lead model
        crm_id = self.env['ir.model'].search([('model', '=', 'res.partner')])
        
        #create tag
        my_tag_id = self.env['res.partner.category'].create({'name': 'Campaign Tag (' + self.campaign_id.name + ')'})
        
        #create filter
        domain_string = "[['category_id', 'ilike', '" + my_tag_id.name + "']]"
        my_filter_id = self.env['ir.filters'].create({'name': self.campaign_id.name + ' Campaign Filter','object_id':crm_id[0].id,'model_id':'crm.lead','domain':domain_string})
        
        #create segment
        new_seg = self.env['marketing.campaign.segment'].create({'name': self.campaign_id.name,'campaign_id':self.campaign_id.id,'sync_mode':'create_date','ir_filter_id':my_filter_id.id})
        new_seg.state_running_set()
        
        #create form
        new_form_id = self.env['html.formgen'].create({'name': self.name,'campaign_id':self.campaign_id.id,'tag_id':my_tag_id.id})
        
        #get the id of contact_name and email_from        
        contact_name = self.env['ir.model.fields'].search([('name', '=', 'name'),('model_id.model', '=', 'res.partner')])
        email_from = self.env['ir.model.fields'].search([('name', '=', 'email'),('model_id.model', '=', 'res.partner')])
        
        #insert contact_name and email_from as fields
        self._cr.execute('INSERT INTO html_formgen_ir_model_fields_rel VALUES(%s,%s)',(new_form_id.id,contact_name.id,))
        self._cr.execute('INSERT INTO html_formgen_ir_model_fields_rel VALUES(%s,%s)',(new_form_id.id,email_from.id,))
        #new_form_id._generate_form()

        return {
	                    'name': 'Customer Invoices',
	                    'view_type': 'form',
	                    'view_mode': 'form',
	                    'res_model': 'html.formgen',
	                    'type': 'ir.actions.act_window',
	                    'res_id': new_form_id.id or False,
               }
class html_gen(models.Model):

    _name = "html.formgen"

    name = fields.Char(string='Form Name', required='True', readonly=True)
    campaign_id = fields.Many2one('marketing.campaign', required='True', string='Campaign', readonly=True)
    fields_ids = fields.Many2many('ir.model.fields', domain="['|',('ttype','=','char'),'|',('ttype','=','text'),('ttype','=','integer'),('name','!=','create_date'),('name','!=','create_uid'),('name','!=','id'),('name','!=','write_date'),('name','!=','write_uid'),('model_id.model','=','res.partner')]",string="Form Fields")
    output_html = fields.Text(string='Embed Code')
    tag_id = fields.Many2one('crm.case.categ', readonly=True)
    thank_url = fields.Char(string='Thank You Page URL')
    form_type = fields.Selection([('opt','Optimize Press'),('odoo','Odoo Website')], string="Form Type")



    @api.one
    def generate_form(self):
        if self.form_type == 'opt':
            self.generate_form_optimize()
        elif self.form_type == 'odoo':
            self.generate_form_odoo()
        else:
            self.generate_form_optimize()
        
    
    @api.one
    def generate_form_odoo(self):
        html_output = ""
        html_output += '<div id="contact_body">' + "\n"
        html_output += '<form method="POST" class="form-horizontal mt32" action="' + request.httprequest.host_url + 'form/myinsert">' + "\n"
        html_output += '<input type="hidden" name="form_id" value="' + str(self.id) + '"/>' + "\n"



            

        for ff in self.fields_ids:
            
            html_output += "<div t-attf-class=\"form-group #{error and 'name' in error and 'has-error' or ''}\">\n"
	    html_output += "<label class=\"col-md-3 col-sm-4 control-label\" for=\"" + ff.name + "\">" + ff.field_description
	    
	    if ff.required == True:
                html_output += ' *'
                
	    html_output += "</label>\n"
	    
	    html_output += "<div class=\"col-md-7 col-sm-8\">\n";
            
            if ff.ttype == "char":

                html_output += '<input class="form-control" type="text" name="' + ff.name + '"'
                
                if ff.size > 0:
                    html_output += ' maxlength="' + ff.size + '"'
                
                if ff.required == True:
                    html_output += ' required="required"'
            
                html_output += '/>\n'
                
            if ff.ttype == "text":
                html_output += '<textarea class="form-control" name="' + ff.name + '"'
               
                if ff.required == True:
	            html_output += ' required="required"'
	                
	        html_output += '></textarea>\n'
	    if ff.ttype == "integer":
                html_output += '<input class="form-control" type="number" name="' + ff.name + '"'
               
                if ff.required == True:
	            html_output += ' required="required"'
	                
	        
	    
	    html_output += "</div>\n"
            html_output += "</div>\n"
	html_output += "<div class=\"form-group\">\n"
        html_output += "<div class=\"col-md-offset-3 col-sm-offset-4 col-sm-8 col-md-7\">\n"
        html_output += "<button class=\"btn btn-primary btn-lg\">Send</button>\n"
        html_output += "</div>\n"
        html_output += "</div>\n"
	html_output += "</form>\n"        
        html_output += "</div>"
        self.output_html = html_output



    
    @api.one
    def generate_form_optimize(self):
        html_output = ""
        html_output += '<div id="contact_body">' + "\n"
        html_output += '<form method="POST" action="' + request.httprequest.host_url + 'form/myinsert">' + "\n"
        html_output += '<input type="hidden" name="form_id" value="' + str(self.id) + '"' + "\n"
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
	html_output += "</form>\n"        
        html_output += "</div>"
        self.output_html = html_output
    
    @api.one
    def generate_form_json(self):
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
        
        