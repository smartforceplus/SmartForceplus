from openerp.osv import fields, osv
from openerp.tools.translate import _

class partner_bank_changes_ept(osv.osv):
    _inherit = 'res.partner.bank'
    
    _columns = {
                'bank' : fields.char('Bank', size = 128)
                }
    
    def check_iban(self, cr, uid, ids, context=None):
        return True
    
    def _check_bank(self, cr, uid, ids, context=None):
        return True
    
    _constraints = [
        (check_iban,'Field is removed', ["iban"]),
        (_check_bank, '\nPlease define BIC/Swift code on bank for bank type IBAN Account to make valid payments', ['bic'])
    ]
    
partner_bank_changes_ept()