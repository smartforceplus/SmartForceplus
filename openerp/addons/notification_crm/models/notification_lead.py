#coding: utf-8
from openerp import models, fields, api, _
from openerp import SUPERUSER_ID
from datetime import datetime, timedelta, date

class notification_lead(models.Model):
    _name = "notification.lead"
    _inherit = 'mail.thread'

    name = fields.Char(string='Name',default=_('Reminder'))
    lead_ids= fields.One2many('crm.lead', 'notification_lead_re_id', 'Lead with warning')
    user_id= fields.Many2one('res.users', 'User notification')
    

    @api.model
    def _send_overdue_list(self,lead_notify=False,templ_id=False,subj=_('Leads Reminder')):
        res = True
        if templ_id and lead_notify:
            local_context = self.env.context.copy()
            company = self.env['res.users'].browse(SUPERUSER_ID).company_id.name
            local_context.update({
                'dbname': self.env.cr.dbname,
                'base_url': self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069', context=self.env.context),
                'datetime' : datetime,
                'company' : company,
                'only_user_sign' : True,
            })
            temp_obj = self.env['email.template']
            template_id = self.env['ir.model.data'].get_object('notification_crm', templ_id)
            for notify in lead_notify:
                lang = 'en_EN'
                if notify.user_id.lang:
                    lang = notify.user_id.lang
                local_context.update({'lang':lang,})
                template_id = temp_obj.with_context(local_context).browse(template_id.id)
                body_html = temp_obj.with_context(local_context).render_template(template_id.body_html, 'notification.lead', notify.id)             
                res = notify.with_context(local_context).message_post(
                    body=body_html,
                    subject=subj,
                    subtype='notification_crm.mt_lead_itl_notify',
                    partner_ids=[notify.user_id.partner_id.id],)
        return res 

    
    @api.model    
    def cron_notify(self):
        user_obj = self.env['res.users']
        user_ids = user_obj.search([('active','=',True)])
        stage_ids = self.env['crm.case.stage'].search([('is_notify','=',True)])
        today_date = datetime.now().date()
        notify_ids = []
        for user in user_ids:
            lead_ids = self.env['crm.lead'].search([('date_action','<=',today_date),('stage_id','in',stage_ids.ids),('user_id','=',user.id)])
            if lead_ids:
                notify_id = self.create({'lead_ids':[(6,0,lead_ids.ids)],'user_id': user.id})
                if notify_id:
                    notify_ids.append(notify_id)
            
        self._send_overdue_list(lead_notify=notify_ids,templ_id='crm_lead_overdue_notification',subj=_('Overdue Leads'))
        for notify in notify_ids:
            notify.unlink()
       