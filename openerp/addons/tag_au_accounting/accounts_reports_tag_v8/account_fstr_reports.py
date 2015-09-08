from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import datetime
from dateutil import parser
import openerp.netsvc
import base64
import time
import os

class schedule_account_reports(osv.osv):
    _name = 'schedule.account.reports'
    
    def schedule_report_print(self, cr, uid, *args): #args[0] = ids of reports to print, args[1] = target_moves ('posted', or , 'all'), args[2] = hide zero (True or False), arg[3] = Opening period id
        email_to = ''
        email_person_name = ''
        attachment_name = ''
        report_entries = ''
        report_fiscal_year = ''
        report_period_from = ''
        report_period_to = ''
        
        #Get Root node
        value_id = self.pool.get('ir.model.data').search(cr, uid, [('name', '=', 'tag_account_report_group_ept')])
        if value_id:
            group_id = self.pool.get('ir.model.data').browse(cr, uid, value_id[0]).res_id
            group_obj = self.pool.get('res.groups').browse(cr, uid, group_id)
            #Get user id in group
            project_user_ids = [x.id for x in group_obj.users]
            if project_user_ids:
                for user_partner_obj in self.pool.get('res.users').browse(cr, uid, project_user_ids):
                    email_body = 'Hello %s, <br/><br/> Here are the reports of accounts. Please review it.<br/<br/><hr/>' %(user_partner_obj.name)
                    email_subject = 'Following are reports of Profit & Loss And Balance Sheet for all posted entries.'
                    for j in range(len(args[0])):
                        for obj in self.pool.get('account_fstr.category').browse(cr, user_partner_obj.id, [args[0][j]]):
                            attachment_name = obj.name
                        root_node = args[0][j]
                        #Creating record for account_fstr.wizard
                        date_obj = datetime.datetime.now()
                        #Get fiscal year id 
                        fiscal_year_id = self.pool.get('account.fiscalyear').search(cr, uid, [('company_id' ,'=', user_partner_obj.company_id.id)], order='date_stop desc')
                        if not fiscal_year_id:
                            return False
                        else:
                            for fiscal_obj in self.pool.get('account.fiscalyear').browse(cr, uid, fiscal_year_id):
                                if datetime.datetime.now() >= parser.parse(fiscal_obj.date_start) and datetime.datetime.now() <= parser.parse(fiscal_obj.date_stop):
                                    current_fiscal_id = fiscal_obj.id
                                    break
                        report_fiscal_year = '%d-%d' %(date_obj.year, date_obj.year + 1)
                        if args[1] == 'posted':
                            report_entries = 'All Posted Entries'
                        elif args[1] == 'all':
                            report_entries = 'All Entries'
                        target_move = args[1]
                        hide_zero = args[2] #Boolean True or False
                        #Creating record
                        report_ids = self.pool.get('account_fstr.wizard').create(cr, user_partner_obj.id, {
                                                                                            'hide_zero' : hide_zero,
                                                                                            'root_node' : root_node,
                                                                                            'target_move' : target_move,
                                                                                            'fiscalyear' : current_fiscal_id,
                                                                                            })
                        #Get period_to
                        update_vals = self.pool.get('account_fstr.wizard').onchange_fiscalyear(cr, user_partner_obj.id,[report_ids], current_fiscal_id)
                        #Update record
                        self.pool.get('account_fstr.wizard').write(cr, user_partner_obj.id, report_ids, update_vals.get('value'))
                        #Call function to print report
                        context = {}
                        report = self.pool.get('account_fstr.wizard').print_template(cr, user_partner_obj.id, [report_ids])
                        report['context']['account_fstr_root_node'] = [report['context']['account_fstr_root_node'][0]]
                        report['context']['lang'] = 'en_US'
                        report['context']['active_id'] = report_ids
                        report['context']['active_ids'] = [report_ids]
                        report['context']['ept_html_flag'] = True
#                        ret_file_name = '/tmp/'+ attachment_name +'.pdf'
                        service = netsvc.LocalService("report.Account HTML Report")
                        (result, format) = service.create(cr, user_partner_obj.id, [report_ids], report['datas'], report['context'])
                        email_body += result
#                        fp = open(ret_file_name, 'wb+');
#                        try:
#                            fp.write(result);
#                        except Exception, e:
#                            print e 
#                        finally:
#                            fp.close();
#                        #Get file data
#                        file_obj = open('/tmp/%s.pdf' %(attachment_name), 'rb')
#                        file_data_temp = base64.encodestring(file_obj.read())
                        
                        
                        
                    #Get Account receivable report
                    ar_id = self.pool.get('account.aged.trial.balance').create(cr, uid, {
                                                                                         'chart_account_id' : self.pool.get('account.account').search(cr, uid, [('company_id', '=', user_partner_obj.company_id.id)], order="id", limit=1)[0] or False,
                                                                                         'result_selection' : 'customer',
                                                                                         'date_from' : datetime.datetime.now(),
                                                                                         'direction_selection' : 'past',
                                                                                         'period_length' : 30,
                                                                                         }, context=context)
                    report_ar = self.pool.get('account.aged.trial.balance').check_report(cr, uid, [ar_id], context=context)
#                    report_ar['used_context']['ept_html_flag'] = True
                    report_ar['datas']['form'].get('used_context').update({
                                                                  'ept_html_flag' : True
                                                                  })
                    service = netsvc.LocalService("report.Aged Partner Balance")
                    (result, format) = service.create(cr, user_partner_obj.id, [ar_id], report_ar['datas'], report_ar['datas']['form'].get('used_context'))
                    email_body += "<center><span class='title' style = 'font-size:19pt;'><b>Account Receivable</b></span></center></br>"
                    email_body += "<br/>" + result
                    
                    #Get Account payable report
                    ap_id = self.pool.get('account.aged.trial.balance').create(cr, uid, {
                                                                                         'result_selection' : 'supplier',
                                                                                         'chart_account_id' : self.pool.get('account.account').search(cr, uid, [('company_id', '=', user_partner_obj.company_id.id)], order="id", limit=1)[0] or False,
                                                                                         'date_from' : datetime.datetime.now(),
                                                                                         'direction_selection' : 'past',
                                                                                         'period_length' : 30,
                                                                                         }, context=context)
                    report_ap = self.pool.get('account.aged.trial.balance').check_report(cr, uid, [ap_id], context=context)
                    report_ap['datas']['form'].get('used_context').update({
                                                                  'ept_html_flag' : True
                                                                  })
                    service = netsvc.LocalService("report.Aged Partner Balance")
                    (result, format) = service.create(cr, user_partner_obj.id, [ar_id], report_ap['datas'], report_ap['datas']['form'].get('used_context'))
                    email_body += "<br/><hr/><center><span class='title' style = 'font-size:19pt;'><b>Account Payable</b></span></center><br/>"
                    email_body += result
                    
                    
                    key_values = self.pool.get('ir.config_parameter').search(cr, uid, [('key', '=', 'account_report_email')])
                    for email_from_obj in self.pool.get('ir.config_parameter').browse(cr, uid, key_values):
                        email_from = email_from_obj.value
                        email_to = str(user_partner_obj.partner_id.email or '').encode('utf8')
#                        email_subject =  attachment_name + ' Report for the period starting %s to %s for %s ' %(report_period_from, report_period_to, report_entries) 
                        model = 'schedule.account.reports'
#                            attachment = {}
#                            attachment.update({
#                                               '%s.pdf' %(attachment_name) : base64.decodestring(file_data_temp),
#                                               })
#                            attachment_ids = []
#                            attachment_ids.append(('%s.pdf' %(attachment_name), base64.decodestring(file_data_temp)))
                        ir_mail_server = self.pool.get('ir.mail_server')
                        msg = ir_mail_server.build_email(email_from, [email_to], email_subject, email_body, subtype='html')
                        if ir_mail_server.send_email(cr, uid, msg):
                            email_status = 'sent'
                        else:
                            email_status = 'exception'
                        mail_message_id = self.pool.get('mail.mail').create(cr, uid, {
                                                           'subject' : email_subject,
                                                           'email_from' : email_from,
                                                           'email_to' : email_to,
                                                           'auto_delete' : False,
                                                           'body_html' : email_body,
                                                           'model' : model,
                                                           'state' : email_status,
                                                           'author_id' : user_partner_obj.partner_id.id,
                                                           'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                                                           })
#                        file_obj.close()
#                        os.unlink('/tmp/%s.pdf' %(attachment_name))
        return True
schedule_account_reports()