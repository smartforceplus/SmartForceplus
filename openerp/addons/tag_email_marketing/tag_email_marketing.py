from openerp import models, fields, api
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime

class tag_email_marketing(models.Model):

    _inherit = "mail.mass_mailing"
    
    lang = fields.Char('Language', help="Optional translation language (ISO code) to select when sending out an email. If not set, the english version will be used. This should usually be a placeholder expression that provides the appropriate language, e.g. ")
    mail_server_id = fields.Many2one('ir.mail_server', string="Outgoing Mail Server", readonly=False, help="Optional preferred server for outgoing mails. If not set, the highest priority one will be used.")
    auto_delete = fields.Boolean('Auto Delete', help="Permanently delete this email after sending it, to save space")
    report_template = fields.Many2one('ir.actions.report.xml', string="Optional report to print and attach")
    report_name = fields.Char(string="Report Filename", translate=True, help="Name to use for the generated report file (may contain placeholders)\n The extension can be omitted and will then come from the report type.")
    model_object_field = fields.Many2one('ir.model.fields', string="Field", help="Select target field from the related document model.\n If it is a relationship field you will be able to select a target field at the destination of the relationship.")
    sub_object = fields.Many2one('ir.model', 'Sub-model', readonly=True, help="When a relationship field is selected as first field, this field shows the document model the relationship goes to.")
    sub_model_object_field = fields.Many2one('ir.model.fields', string="Sub-field", help="When a relationship field is selected as first field, this field lets you select the target field within the destination document model (sub-model).")
    null_value = fields.Char(string="Default Value", help="Optional value to use if the target field is empty")
    copyvalue = fields.Char(string="Placeholder Expression", help="Final placeholder expression, to be copy-pasted in the desired template field.")
    
    
    
    @api.v7
    def onchange_sub_model_object_value_field(self, cr, uid, ids, model_object_field, sub_model_object_field=False, null_value=None, context=None):
        result = {
                'sub_object': False,
                'copyvalue': False,
                'sub_model_object_field': False,
                'null_value': False
                }
        if model_object_field:
            fields_obj = self.pool.get('ir.model.fields')
            field_value = fields_obj.browse(cr, uid, model_object_field, context)
            if field_value.ttype in ['many2one', 'one2many', 'many2many']:
                res_ids = self.pool.get('ir.model').search(cr, uid, [('model', '=', field_value.relation)], context=context)
                sub_field_value = False
                if sub_model_object_field:
                    sub_field_value = fields_obj.browse(cr, uid, sub_model_object_field, context)
                if res_ids:
                    result.update({
                        'sub_object': res_ids[0],
                        'copyvalue': self.build_expression(field_value.name, sub_field_value and sub_field_value.name or False, null_value or False),
                        'sub_model_object_field': sub_model_object_field or False,
                        'null_value': null_value or False
                        })
            else:
                result.update({
                        'copyvalue': self.build_expression(field_value.name, False, null_value or False),
                        'null_value': null_value or False
                        })
        return {'value': result}
        
        
    @api.v7
    def build_expression(self, field_name, sub_field_name, null_value):
        """Returns a placeholder expression for use in a template field,
           based on the values provided in the placeholder assistant.

          :param field_name: main field name
          :param sub_field_name: sub field name (M2O)
          :param null_value: default value if the target value is empty
          :return: final placeholder expression
        """
        expression = ''
        if field_name:
            expression = "${object." + field_name
            if sub_field_name:
                expression += "." + sub_field_name
            if null_value:
                expression += " or '''%s'''" % null_value
            expression += "}"
        return expression