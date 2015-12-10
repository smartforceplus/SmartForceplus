from openerp import models, fields, api
from datetime import datetime, timedelta
import openerp
import pytz
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)

class account_invoice_unpaid(models.Model):

    _inherit = "account.invoice"
 
    @api.model
    def tag_email_unpaid_invoices(self):
        email_template = self.env['ir.model.data'].get_object('tag_daily_unpaid_invoice_report', 'tag_report_unpaid_invoices')        
	anthony = self.env['res.partner'].search([('email','=','anthony@anthonygardiner.com')])[0]
	values = self.env['email.template'].generate_email(email_template.id, anthony.id)
	
        unpaid_invoices = self.env['account.invoice'].search([('state','=','open')])
        
        values['body_html'] += "<br/><table style='width:100%;'>"
        values['body_html'] += "<tr><td>Customer</td><td>Number</td><td>Total Amount</td><td>Amount Paid</td></tr>"
                
        for inv in unpaid_invoices:
            values['body_html'] += "<tr><td>" + str(inv.partner_id.name) + "</td><td>" + str(inv.number) + "</td><td>" + str(inv.amount_total) + "</td><td>" + str(inv.residual) + "</td></tr>"
            
        values['body_html'] += "</table>"
	msg_id = self.env['mail.mail'].create(values)
        self.env['mail.mail'].send([msg_id], True)