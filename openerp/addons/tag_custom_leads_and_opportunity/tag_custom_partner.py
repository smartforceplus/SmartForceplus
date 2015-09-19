from openerp.osv import fields, osv
from openerp.addons.crm import crm

class tag_customer_tabs(osv.osv):

    _inherit = "res.partner"

        
    _columns = {

        'user_id_n': fields.many2one('res.users', 'Salesperson', select=True, track_visibility='always'),
        'industry': fields.many2one('industry', 'Industry', select=True),
		'status': fields.many2one('status', 'Status', select=True),
        'parent_id': fields.many2one('res.partner', 'Related Company', select=True, track_visibility='always'),
		'lastname': fields.char('Last Name', size=64, select=True, track_visibility='always'),
		'birth_date': fields.date('Birth Date', help="Send a birthday wish?", select=True, track_visibility='always'),
        'street_n': fields.char('Street', select=True, track_visibility='always'),
        'street2_n': fields.char('Street2', select=True, track_visibility='always'),
        'zip_n': fields.char('Zip', size=24, change_default=True, select=True, track_visibility='always'),
        'city_n': fields.char('City', select=True, track_visibility='always'),
        'state_id_n': fields.many2one("res.country.state", 'State', ondelete='restrict', select=True, track_visibility='always'),
        'country_id_n': fields.many2one('res.country', 'Country', ondelete='restrict', select=True, track_visibility='always'),
        'email_form': fields.char('Email', select=True, track_visibility='always'),
        'phone_num': fields.char('Phone', select=True, track_visibility='always'),
        'fax_num': fields.char('Fax', select=True, track_visibility='always'),
        'tag_crm_states': fields.selection([('1','Lead'), ('2','Customer'),('3','Referral')], 'Contact Status'),
        'mobile_num': fields.char('Mobile', select=True, track_visibility='always'),
        'vehicle_name_n': fields.char('Vehicle', size=64, select=True, track_visibility='always'),
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
		'TF2': fields.char('ABN', size=30), 
		'TF3': fields.char('ACN', size=30),
		'TF4a': fields.char('TF4a', size=50), 		
		'TF5': fields.char('TF5', size=100), 
		'TF6': fields.char('TF6', size=100), 
		'TF7': fields.char('TF7', size=25), 
		'TF8': fields.char('TF8', size=25),
		'TF9': fields.date('Birthdate', size=100), 
		'TF10': fields.char('BRM Site', size=50), 
		'TF11': fields.char('Init BRM Pass', size=20), 
		'TF12': fields.char('Website', size=50),
		'TF13': fields.char('Access Email', size=50),
		'TF14': fields.date(' TF14'), 
		'TF15': fields.float('TF15'), 
		'TF16': fields.char('TF16',size=25), 
		'TF17': fields.char('TF17', size=25), 
		'TF18': fields.char('TF18', size=5),
		'TF19': fields.char('TF19', size=25), 
		'TF20': fields.char('TF20', size=25),
		'TF21': fields.char('TF21', size=25),
		'TF22': fields.char('TF22', size=25), 
		'TF23': fields.char('TF23', size=25), 
		'TF24': fields.selection([('1','Choice 1'), ('2','Choice 2'), ('3','Choice 3'),('4','Choice 4')],'TF24'),
		'TF25': fields.selection([('1','Choice 1'), ('2','Choice 2')], 'TF 25'),
		'TF26': fields.selection([('1','Choice 1'), ('2','Choice 2'),('3','Choice 3')], 'TF26'),
		'TF27': fields.char('TF27', size=25), 
		'TF28': fields.char('TF28', size=200), 
		'TF29': fields.char('TF29', size=25), 
		'TF30': fields.char('TF30', size=25),
		'TF31': fields.char('TF31', size=25),
		'TF32': fields.char('TF32', size=25), 
		'TF33': fields.char('TF33', size=25),
		'TF34': fields.char('TF34', size=30), 
		'TF35': fields.char('TF35', size=30),
		'TF36': fields.char('TF36', size=25),
		'TF37': fields.char('TF37', size=25), 
		'TF38': fields.char('TF38', size=25), 
		'TF39': fields.char('TF39', size=25), 
		'TF40': fields.char('TF40', size=25), 
		'TF41': fields.char('TF41', size=25),
		'TF42': fields.selection([('1','Choice 1'), ('2','Choice 2'), ('3','Choice 3'),('4','Choice 4')],'TF42'), 
		'TF43': fields.selection([('1','Choice 1'), ('2','Choice 2')], 'TF43'), 
		'TF44': fields.selection([('1','Choice 1'), ('2','Choice 2'),('3','Choice 3')], 'TF44'), 
		'TF45': fields.char('TF45', size=25),
		'TF46': fields.char('TF46', size=100),
		'TF47': fields.char('TF47', size=30), 
		'TF48': fields.char('TF48', size=30),
		'TF49': fields.char('TF49', size=25), 
		'TF50': fields.char('TF50', size=25),
	    'T1Label1': fields.char('T1Label1', size=15),
	    'T1F1': fields.float('T1F1'),
        'T1F2': fields.float('T1F2'), 
        'T1F3': fields.float('T1F3'), 
        'T1F4': fields.float('T1F4'), 
        'T1F5': fields.float('T1F5'),
        'T1F6': fields.float('T1F6'),
	    'T1F7': fields.float('T1F7'), 
	    'T1F8': fields.float('T1F8'),
	    'T1F9': fields.float('T1F9'), 
	    'T1F10': fields.float('T1F10'),
	    'T1F11': fields.float('T1F11'),
        'T1F12': fields.float('T1F12'), 
        'T1F13': fields.float('T1F13'), 
        'T1F14': fields.float('T1F14'), 
        'T1F15': fields.float('T1F15'),
        'T1F16': fields.float('T1F16'),
	    'T1Label2': fields.char('T1Label2', size=15),
	    'T1F17': fields.float('T1F17'),
        'T1F18': fields.float('T1F18'), 
        'T1F19': fields.float('T1F19'), 
        'T1F20': fields.float('T1F20'), 
        'T1F21': fields.float('T1F21'),
        'T1F22': fields.float('T1F22'),
	    'T1F23': fields.float('T1F23'), 
	    'T1F24': fields.float('T1F24'),
	    'T1F25': fields.float('T1F25'), 
	    'T1F26': fields.float('T1F26'),
	    'T1F27': fields.float('T1F27'),
        'T1F28': fields.float('T1F28'), 
        'T1F29': fields.float('T1F29'), 
        'T1F30': fields.float('T1F30'), 
        'T1F31': fields.float('T1F31'),
        'T1F32': fields.float('T1F32'),
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
        'TagList101': fields.char('TPL01'),
        'TagList102': fields.char('TPL02'),
		'TagList103': fields.char('TPL03'),
		'TagList104': fields.char('TPL04'),
		'TagList105': fields.char('TPL05', size=20),
		'TagList106': fields.text('TPL06', size=150),
		'TagList107': fields.char('TPL07'),
		'TagList108': fields.char('TPL08'),
		'TagList109': fields.char('TPL09'),	
		'TagList110': fields.char('TPL10')
    }


class tag_cust_list_2(osv.osv):

    _name = "res.partner.tag_partnerlist_2"
    
    _columns = {
        'tag_partnerlist2_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList201': fields.char('PL201'),
        'TagList202': fields.char('PL202'),
        'TagList203': fields.char('PL203'),
        'TagList204': fields.char('PL204'),
        'TagList205': fields.char('PL205'),
        'TagList206': fields.char('PL206'),
		'TagList207': fields.char('PL207'),
		'TagList208': fields.char('PL208'),
		'TagList209': fields.char('PL209'),	
		'TagList210': fields.char('PL210')			
    }

class tag_cust_list_3(osv.osv):

    _name = "res.partner.tag_partnerlist_3"
    
    _columns = {
        'tag_partnerlist3_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList301': fields.char('PL301'),
        'TagList302': fields.char('PL302'),
        'TagList303': fields.char('PL303'),
        'TagList304': fields.char('PL304'),
        'TagList305': fields.char('PL305'),
        'TagList306': fields.char('PL306'),
        'TagList307': fields.float('PL307')
    }
    

class tag_cust_list_4(osv.osv):

    _name = "res.partner.tag_partnerlist_4"
    
    _columns = {
        'tag_partnerlist4_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList401': fields.char('PL401'),
        'TagList402': fields.char('PL402'),
        'TagList403': fields.char('PL403'),
        'TagList404': fields.char('PL404'),
        'TagList405': fields.text('PL405'),
        'TagList406': fields.char('PL406'),
        'TagList407': fields.float('PL407')
    }
    
class tag_cust_list_5(osv.osv):

    _name = "res.partner.tag_partnerlist_5"
    
    _columns = {
        'tag_partnerlist5_id': fields.many2one('res.partner','Tag Back Reference Field', required=True, readonly=True),
        'TagList501': fields.char('PL501'),
        'TagList502': fields.char('PL502'),
        'TagList503': fields.char('PL503'),
        'TagList504': fields.char('PL504'),
        'TagList505': fields.char('PL505'),
        'TagList506': fields.char('PL506'),
        'TagList507': fields.char('PL507')
    }

class res_partner(osv.osv):

    _inherit = "res.partner"

    _columns = {

        'vehicle_name':fields.char('Vehicle',size=32),

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
