from openerp.osv import fields, osv

class tag_help(osv.osv):
  _name = "tag.help" 
  _columns = {
		'Location': fields.char('Location', size=128, required=True),
        'Name': fields.char('Name', size=128, required=True),
		'Link': fields.char('Link', size=128, required=True),
		'Action': fields.char('Action', size=128, required=True)
  }
tag_help()