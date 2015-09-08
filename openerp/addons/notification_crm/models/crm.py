from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_case_stage(osv.osv):
    _name = "crm.case.stage"
    _inherit = "crm.case.stage"
    _columns={
        'is_notify':fields.boolean('Send notification',help="Send notification for lead in this stage"),
    }

    _defaults = {
        'is_notify': False,
    }

crm_case_stage()

class crm_lead(osv.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'
    _columns = {
    	'notification_lead_re_id' : fields.many2one('notification.lead', 'Send notification'),
    }

crm_lead()
