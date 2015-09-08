import time
from lxml import etree
import openerp.addons.decimal_precision as dp

from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
import openerp.tools.translate
#from openerp import tools.translate import _

class account_invoice_ept(osv.osv):
    _inherit = 'account.invoice'
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('supplier_invoice_number'):
            vals.update({
                         'supplier_invoice_number' : vals.get('supplier_invoice_number').replace(' ', '')
                         }) 
        return super(account_invoice_ept, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        print '###########3'
        if vals.get('supplier_invoice_number'):
            print '#################################################'
            vals.update({
                         'supplier_invoice_number' : vals.get('supplier_invoice_number').replace(' ', '')
                         })
            print vals
        return super(account_invoice_ept, self).write(cr, uid, ids, vals, context=context)
account_invoice_ept()