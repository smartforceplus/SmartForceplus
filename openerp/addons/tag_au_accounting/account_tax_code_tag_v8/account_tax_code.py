from openerp.osv import fields, osv
class account_tax_code(osv.osv):
    _name = 'account.tax.code'
    _inherit = 'account.tax.code'
    
    def _sum_period(self, cr, uid, ids, name, args, context):
        if context is None:
            context = {}
        move_state = ('posted', )
        if context.get('state', False) == 'all':
            move_state = ('draft', 'posted', )
        if context.get('period_id', False):
            period_id = context['period_id']
        elif context.get('periods'):
            periods = context.get('periods')
            return self._sum(cr, uid, ids, name, args, context,
                where=' AND line.period_id IN %s AND move.state IN %s', where_params=(tuple(periods), move_state))
        else:
            period_id = self.pool.get('account.period').find(cr, uid)
            if not period_id:
                return dict.fromkeys(ids, 0.0)
            period_id = period_id[0]
        return self._sum(cr, uid, ids, name, args, context,
                where=' AND line.period_id=%s AND move.state IN %s', where_params=(period_id, move_state))
    _columns = {
                    'type_ept':fields.selection([('view','View'),('normal','Normal')], 'Type'),
                    'sum_period': fields.function(_sum_period, string="Period Sum"),
                }
    _defaults = {
                    'type_ept':'view',
                 }
account_tax_code()