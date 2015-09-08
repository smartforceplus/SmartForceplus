from openerp.osv import fields, osv

class tag_custom_opportunity(osv.osv):

  _inherit = "crm.lead"

  _columns = {
    'firstname':fields.char('First Name', size=50),
    'lastname':fields.char('Last Name', size=50),
    'refer' : fields.many2one('res.partner', 'Refferal Partners', select=True),
    'industry': fields.many2one('industry', 'Industry', select=True),
	'namecom': fields.many2many('marketing.campaign','campaign_compagn_reli','crm_lead_id','marketing_campaign_id','Campaign'),
        'user_id_n': fields.many2one('res.users', 'Salesperson', select=True, track_visibility='always'),
        'industry': fields.many2one('industry', 'Industry', select=True),
		'firstname': fields.char('Contact Name', size=64, select=True, track_visibility='always'),
        'parent_id': fields.many2one('res.partner', 'Related Company', select=True, track_visibility='always'),
        'contact_name': fields.char('Contact Name', size=64, select=True, track_visibility='always'),
		'lastname': fields.char('Last Name', size=64, select=True, track_visibility='always'),
        'street_n': fields.char('Street', select=True, track_visibility='always'),
        'street2_n': fields.char('Street2', select=True, track_visibility='always'),
        'zip_n': fields.char('Zip', size=24, change_default=True, select=True, track_visibility='always'),
        'city_n': fields.char('City', select=True, track_visibility='always'),
        'state_id_n': fields.many2one("res.country.state", 'State', ondelete='restrict', select=True, track_visibility='always'),
        'country_id_n': fields.many2one('res.country', 'Country', ondelete='restrict', select=True, track_visibility='always'),
        'email_form': fields.char('Email', select=True, track_visibility='always'),
        'phone_num': fields.char('Phone', select=True, track_visibility='always'),
        'fax_num': fields.char('Fax', select=True, track_visibility='always'),
        'mobile_num': fields.char('Mobile', select=True, track_visibility='always'),
        'vehicle_name_n': fields.char('Vehicle', size=64, select=True, track_visibility='always'),
        'date_deadline': fields.date('Expected Closing', help="Estimate of the date on which the opportunity will be won.", select=True, track_visibility='always'),
        'date_action': fields.date('Next Action Date', select=True, track_visibility='always'),
        
        'categ_ids': fields.many2many('crm.case.categ', 'res_partner_category_rel', 'partner_id', 'category_id', 'Tags', \
            domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", select=True, track_visibility='always'),
        'title_action': fields.char('Next Action', select=True, track_visibility='always'),
        'company_currency': fields.related('company_id', 'currency_id', type='many2one', string='Currency', readonly=True, relation="res.currency"),
        'planned_revenue': fields.float('Expected Revenue', select=True, track_visibility='always'),
        'probability': fields.float('Success Rate (%)', group_operator="avg"),
        'TF1': fields.char('Data Upload ID', size=15),
		'TF2': fields.char('TF 2', size=25), 
		'TF3': fields.text('TF 3', size=50),
		'TF4': fields.date('Settlement Date'), 
		'TF5': fields.float('Loan Term'), 
		'TF6': fields.text('TF 6', size=100), 
		'TF7': fields.char('ACN', size=25), 
		'TF8': fields.char('ABN', size=25),
		'TF9': fields.text('TF 9', size=100), 
		'TF10': fields.text('TF 10', size=50), 
		'TF11': fields.char('TF 11', size=100), 
		'TF12': fields.char('Website', size=50),
		'TF13': fields.char('Other 13', size=25),
		'TF14': fields.date(' TF 14'), 
		'TF15': fields.float('TF 15'), 
		'TF16': fields.char('TF 16',size=25), 
		'TF17': fields.char('TF 17', size=25), 
		'TF18': fields.char('TF 18', size=5),
		'TF19': fields.char('TF 19', size=25), 
		'TF20': fields.char('TF 20', size=25),
		'TF21': fields.char('TF 21', size=25),
		'TF22': fields.char('TF 22', size=25), 
		'TF23': fields.char('TF 23', size=25), 
		'TF24': fields.selection([('1','Choice 1'), ('2','Choice 2'), ('3','Choice 3'),('4','Choice 4')],'TF 24'),
		'TF25': fields.selection([('1','Choice 1'), ('2','Choice 2')], 'TF 25'),
		'TF26': fields.selection([('1','Choice 1'), ('2','Choice 2'),('3','Choice 3')], 'TF 26'),
		'TF27': fields.char('TF 27', size=25), 
		'TF28': fields.char('TF 28', size=25),  
		'TF29': fields.char('TF 29', size=25), 
		'TF30': fields.char('TF 30', size=25),
		'TF31': fields.char('TF 31', size=25),
		'TF32': fields.char('TF 32', size=25), 
		'TF33': fields.char('TF 33', size=25),
		'TF34': fields.char('TF 34', size=30), 
		'TF35': fields.char('TF 35', size=30),
		'TF36': fields.char('TF 36', size=25),
		'TF37': fields.char('TF 37', size=25), 
		'TF38': fields.char('TF 38', size=25), 
		'TF39': fields.char('TF 39', size=25), 
		'TF40': fields.char('TF 40', size=25), 
		'TF41': fields.char('TF 41', size=25),
		'TF42': fields.selection([('1','Choice 1'), ('2','Choice 2'), ('3','Choice 3'),('4','Choice 4')],'TF 42'), 
		'TF43': fields.selection([('1','Choice 1'), ('2','Choice 2')], 'TF 43'), 
		'TF44': fields.selection([('1','Choice 1'), ('2','Choice 2'),('3','Choice 3')], 'TF 44'), 
		'TF45': fields.char('TF 45', size=25),
		'TF46': fields.char('TF 46', size=100),
		'TF47': fields.char('TF 47', size=30), 
		'TF48': fields.char('TF 48', size=30),
		'TF49': fields.char('TF 49', size=25), 
		'TF50': fields.char('TF 50', size=25),
    'TagCustAL1': fields.float('List Opt 1'),
    'TagCustAL2': fields.float('List Opt 2'), 
    'TagCustAL3': fields.float('List Opt 3'), 
    'TagCustAL4': fields.float('List Opt 4'), 
    'TagCustAL5': fields.float('List Opt 5'),
    'TagCustAL6': fields.float('List Opt 6'),
    'TagCustAL7': fields.float('List Opt 7'), 
    'TagCustAL8': fields.float('List Opt 8'),
    'TagCustAL9': fields.float('List Opt 9'), 
    'TagCustAL9a': fields.float('List Opt 9a'),
    'TagCustAL9b': fields.float('List Opt 9b'),
    'TagCustAL9c': fields.float('List Opt 9c'),
    'TagCustAL9d': fields.float('List Opt 9d'),
    'TagCustAL10': fields.float('List Opt 10'),
    'TagCustAL11': fields.float('List Opt 11'),
    'TagCustAL12': fields.float('List Opt 12'), 
    'TagCustAL13': fields.float('List Opt 13'), 
    'TagCustAL14': fields.float('List Opt 14'), 
    'TagCustAL15': fields.float('List Opt 15'),
    'TagCustAL16': fields.float('List Opt 16'),
    'TagCustL1Label2': fields.char('List Label 1', size=1),
    'TagCustAL21': fields.float('List Opt 21'),
    'TagCustAL22': fields.float('List Opt 22'), 
    'TagCustAL23': fields.float('List Opt 23'), 
    'TagCustAL24': fields.float('List Opt 24'), 
    'TagCustAL25': fields.float('List Opt 25'),
    'TagCustAL26': fields.float('List Opt 26'),
    'TagCustAL27': fields.float('List Opt 27'), 
    'TagCustAL28': fields.float('List Opt 28'),
    'TagCustAL29': fields.float('List Opt 29'), 
    'TagCustAL30': fields.float('List Opt 30'),
    'TagCustAL31': fields.float('List Opt 31'),
    'TagCustAL32': fields.float('List Opt 32'), 
    'TagCustAL33': fields.float('List Opt 33'), 
    'TagCustAL34': fields.float('List Opt 34'), 
    'TagCustAL35': fields.float('List Opt 35'),
    'TagCustAL36': fields.float('List Opt 36'),
    'TagDevNotesFT1':fields.text('DFT1 Notes'),
    'TagDevNotesFT1H':fields.char('Help'),
    'TagDevNotesFT2':fields.text('FT2 Added for comments re development of this tab area'),
    'TagDevNotesFT3':fields.text('FT3 Added for comments re development of this tab area'),
    'TagDevNotesFT4':fields.text('FT4 Added for comments re development of this tab area'),
    'TagDevNotesFT5':fields.text('FT5 Added for comments re development of this tab area'),
    'TagDevNotesLT1':fields.text('LT1 Added for comments re development of this tab area'),
    'TagDevNotesLT2':fields.text('LT2 Added for comments re development of this tab area'),
    'TagDevNotesLT3':fields.text('LT3 Added for comments re development of this tab area'),
    'TagDevNotesLT4':fields.text('LT4 Added for comments re development of this tab area'),
    'TagDevNotesLT5':fields.text('LT5 Added for comments re development of this tab area'),
    'TagCustList01':fields.one2many('crm.lead.tag_cust_list_1', 'tag_list1_id', 'TagListA01'),
    'TagCustList02':fields.one2many('crm.lead.tag_cust_list_2', 'tag_list2_id', 'TagListA02'),
    'TagCustList03':fields.one2many('crm.lead.tag_cust_list_3', 'tag_list3_id', 'TagListA03'),
    'TagCustList04':fields.one2many('crm.lead.tag_cust_list_4', 'tag_list4_id', 'TagListA04'),
    'TagCustList05':fields.one2many('crm.lead.tag_cust_list_5', 'tag_list5_id', 'TagListA05')
  }
  
class tag_cust_list_1(osv.osv):

    _name = "crm.lead.tag_cust_list_1"
    
    _columns = {
        'tag_list1_id': fields.many2one('crm.lead','Tag Back Reference Field', required=True, readonly=True),
        'TagList101': fields.char('L1 Choice 1'),
        'TagList102': fields.char('L1 Choice 4'),
        'TagList103': fields.char('L1 Choice 3'),
        'TagList104': fields.char('L1 Choice 4'),
        'TagList105': fields.char('L1 Choice 5', size=20),
        'TagList106': fields.char('L1 Choice 6', size=150),
		'TagList107': fields.char('L1 Choice 7'),
		'TagList108': fields.char('L1 Choice 8'),
		'TagList109': fields.char('L1 Choice 9'),
		'TagList110': fields.char('L1 Choice 10')
    }
    
class tag_cust_list_2(osv.osv):

    _name = "crm.lead.tag_cust_list_2"
    
    _columns = {
        'tag_list2_id': fields.many2one('crm.lead','Tag Back Reference Field', required=True, readonly=True),
		'TagList201': fields.char('TagList201'),
        'TagList202': fields.char('TagList202'),
        'TagList203': fields.char('TagList203'),
        'TagList204': fields.char('TagList204'),
        'TagList205': fields.char('TagList205'),
        'TagList206': fields.char('TagList206'),
		'TagList207': fields.char('TagList207'),
		'TagList208': fields.char('TagList208'),
		'TagList209': fields.char('TagList209'),
		'TagList210': fields.char('TagList210')
    }

class tag_cust_list_3(osv.osv):

    _name = "crm.lead.tag_cust_list_3"
    
    _columns = {
        'tag_list3_id': fields.many2one('crm.lead','Tag Back Reference Field', required=True, readonly=True),
        'TagList301': fields.char('L3 Choice 1'),
        'TagList302': fields.char('L3 Choice 2'),
        'TagList303': fields.char('L3 Choice 3'),
        'TagList304': fields.char('L3 Choice 4'),
        'TagList305': fields.char('L3 Choice 5'),
        'TagList306': fields.char('L3 Choice 6'),
        'TagList307': fields.char('L3 Choice 7')
    }
    

class tag_cust_list_4(osv.osv):

    _name = "crm.lead.tag_cust_list_4"
    
    _columns = {
        'tag_list4_id': fields.many2one('crm.lead','Tag Back Reference Field', required=True, readonly=True),
        'TagList401': fields.char('L4 Choice 1'),
        'TagList402': fields.char('L4 Choice 2'),
        'TagList403': fields.char('L4 Choice 3'),
        'TagList404': fields.char('L4 Choice 4'),
        'TagList405': fields.text('L4 Choice 5'),
        'TagList406': fields.char('L4 Choice 6'),
        'TagList407': fields.float('L4 Choice 7')
    }
    
class tag_cust_list_5(osv.osv):

    _name = "crm.lead.tag_cust_list_5"
    
    _columns = {
        'tag_list5_id': fields.many2one('crm.lead','Tag Back Reference Field', required=True, readonly=True),
        'TagList501': fields.char('L5 Choice 1'),
        'TagList502': fields.char('L5 Choice 2'),
        'TagList503': fields.char('L5 Choice 3'),
        'TagList504': fields.char('L5 Choice 4'),
        'TagList505': fields.char('L5 Choice 5'),
        'TagList506': fields.char('L5 Choice 6'),
        'TagList507': fields.char('L5 Choice 7')
    }
	
def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        print 'onchange partner idddd'
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            values = {
                'partner_name': partner.parent_id.name if partner.parent_id else partner.name,
                'contact_name': partner.name if partner.parent_id else False,
				'lastname':partner.lastname,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id and partner.state_id.id or False,
                'country_id': partner.country_id and partner.country_id.id or False,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'fax': partner.fax,
                'zip': partner.zip,
            }
        return {'value': values}	
tag_custom_opportunity()