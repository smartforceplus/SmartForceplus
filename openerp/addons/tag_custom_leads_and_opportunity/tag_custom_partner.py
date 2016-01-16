from openerp.osv import fields, osv
from openerp.addons.crm import crm

class tag_customer_tabs(osv.osv):

    _inherit = "res.partner"

        
    _columns = {
        'industry': fields.many2one('industry', 'Industry', select=True),
        'parent_id': fields.many2one('res.partner', 'Related Company', select=True, track_visibility='always'),
	'lastname': fields.char('Last Name', size=64, select=True, track_visibility='always'),
	'birth_date': fields.date('Birth Date', help="Send a birthday wish!", select=True, track_visibility='always'),
        'tag_crm_states': fields.selection([('1','Lead'), ('2','Customer'),('3','Referral')], 'Contact Type'),
        'date_deadline': fields.date('Expected Closing', help="Estimate of the date on which the opportunity will be won.", select=True, track_visibility='always'),
        'date_action': fields.date('Next Action Date', select=True, track_visibility='always'),
        'priority': fields.selection(crm.AVAILABLE_PRIORITIES, 'Priority', select=True, track_visibility='always'),
        'categ_ids': fields.many2many('crm.case.categ', 'res_partner_category_rel', 'partner_id', 'category_id', 'Tags', \
            domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", select=True, track_visibility='always'),
        'title_action': fields.char('Next Action', select=True, track_visibility='always'),
        'company_currency': fields.related('company_id', 'currency_id', type='many2one', string='Currency', readonly=True, relation="res.currency"),
        'planned_revenue': fields.float('Expected Revenue', select=True, track_visibility='always'),
        'probability': fields.float('Success Rate (%)', group_operator="avg"),
		'referred_web_link': fields.char('Referred Web Link', size=100),
		'referral_web_link': fields.char('Referral Web Link', size=100),
		'referred_by': fields.char('Referred By', size=50),
        'TF1': fields.char('Data Upload ID', size=15),
		'abn': fields.char('ABN', size=30), 
		'acn': fields.char('ACN', size=30),
		'TF4a': fields.char('TF4a', size=50), 
	'status': fields.char('Status', size=50), 
	    'TagPartnerList01':fields.one2many('res.partner.tag_partnerlist_1', 'tag_partnerlist1_id', 'TagPartnerList01'),
	    'TagPartnerList02':fields.one2many('res.partner.tag_partnerlist_2', 'tag_partnerlist2_id', 'TagPartnerList02'),
	    'TagPartnerList03':fields.one2many('res.partner.tag_partnerlist_3', 'tag_partnerlist3_id', 'TagPartnerList03'),
	    'TagPartnerList04':fields.one2many('res.partner.tag_partnerlist_4', 'tag_partnerlist4_id', 'TagPartnerList04'),
	    'TagPartnerList05':fields.one2many('res.partner.tag_partnerlist_5', 'tag_partnerlist5_id', 'TagPartnerList05')
    }

    _defaults = {
        'user_id': lambda s, cr, uid, c: uid,
       # 'stage_id': lambda s, cr, uid, c: s._get_default_stage_id(cr, uid, c),
       # 'section_id': lambda s, cr, uid, c: s._get_default_section_id(cr, uid, context=c),
        'priority': lambda *a: crm.AVAILABLE_PRIORITIES[2][0],
        'tag_crm_states':'1',
    
    }

    
class tag_cust_partnerlist_1(osv.osv):

    _name = "res.partner.tag_partnerlist_1"
    
    _columns = {
        'tag_partnerlist1_id': fields.many2one('res.partner','Member Block Reference', required=True, readonly=True),
        'TagList101': fields.char('TPL01')
    }


class tag_cust_list_2(osv.osv):

    _name = "res.partner.tag_partnerlist_2"
    
    _columns = {
        'tag_partnerlist2_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList201': fields.char('PL201')		
    }

class tag_cust_list_3(osv.osv):

    _name = "res.partner.tag_partnerlist_3"
    
    _columns = {
        'tag_partnerlist3_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList301': fields.char('PL301')
    }
    

class tag_cust_list_4(osv.osv):

    _name = "res.partner.tag_partnerlist_4"
    
    _columns = {
        'tag_partnerlist4_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList401': fields.char('PL401')
    }
    
class tag_cust_list_5(osv.osv):

    _name = "res.partner.tag_partnerlist_5"
    
    _columns = {
        'tag_partnerlist5_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList501': fields.char('PL501')
    }
    
class industry(osv.osv):
    _name = "industry"
    _columns = {

        'name':fields.char('Industry',size=50),

    }
    
class status(osv.osv):
    _name = "status"
    _columns = {

        'name':fields.char('Status',size=50),
	'sequence':fields.char('Sequence',size=3),

    }	
	
	
tag_customer_tabs()
