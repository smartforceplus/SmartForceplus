# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class account_fstr_wizard(osv.osv_memory):

    _name = 'account_fstr.wizard'
    _description = "Template Print/Preview"
    _columns = {
        'fiscalyear': fields.many2one('account.fiscalyear', \
                                    'Fiscal year',  \
                                    help = 'Keep empty for all open fiscal years'),
        'period_from': fields.many2one('account.period', 'Start period'),
        'period_to': fields.many2one('account.period', 'End period'),
        'target_move': fields.selection([('posted', 'All Posted Entries'),
                                         ('all', 'All Entries'),
                                        ], 'Target Moves', required = True),
        'root_node': fields.many2one('account_fstr.category', 'Root node', required=True,),
        'hide_zero': fields.boolean('Hide accounts with a zero balance'),
    }

    def default_get(self, cr, uid, fields, context={}):
        result = super(osv.osv_memory, self).default_get(cr, uid, fields, context=context)
        result['root_node']=  context.get('active_id', None)
        return result

    def onchange_fiscalyear(self, cr, uid, ids, fiscalyear_id=False, context=None):
        res = {}
        res['value'] = {}
        if fiscalyear_id:
            start_period = end_period = False
            cr.execute('''
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               ORDER BY p.date_start ASC
                               LIMIT 1) AS period_start
                UNION
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.date_start < NOW()
                               ORDER BY p.date_stop DESC
                               LIMIT 1) AS period_stop''', (fiscalyear_id, fiscalyear_id))
            periods =  [i[0] for i in cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            res['value'] = {'period_from': start_period, 'period_to': end_period}
        return res

    def open_window(self, cr, uid, ids, context=None):
        """
        Opens chart of Accounts
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of account chart’s IDs
        @return: dictionary of Open account chart window on given fiscalyear and all Entries or posted entries
        """
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        period_obj = self.pool.get('account.period')
        fy_obj = self.pool.get('account.fiscalyear')
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        result = mod_obj.get_object_reference(cr, uid, 'account_fstr', 'action_account_fstr_category_tree')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['periods'] = []
        if data['period_from'] and data['period_to']:
            result['periods'] = self.build_ctx_periods(cr, uid,[data['period_from'][0]], [data['period_to'][0]])
        result['context'] = str({'fiscalyear': data['fiscalyear'][0], 'periods': result['periods'], \
                                    'state': data['target_move']})
        if data['fiscalyear']:
            result['name'] += ':' + fy_obj.read(cr, uid, [data['fiscalyear'][0]], context=context)[0]['code']
        result['domain'] = [('id', '=', data['root_node'][0])]
        return result
    
    def build_ctx_periods(self, cr, uid, period_from_id, period_to_id):
        period_obj = self.pool.get('account.period')
        if period_from_id == period_to_id:
            return [period_from_id]
        period_from = period_obj.browse(cr, uid, period_from_id)
        period_date_start = period_from[0].date_start
        company1_id = period_from[0].company_id.id
        period_to = period_obj.browse(cr, uid, period_to_id)
        period_date_stop = period_to[0].date_stop
        company2_id = period_to[0].company_id.id
        if company1_id != company2_id:
            raise osv.except_osv(_('Error'), _('You should have chosen periods that belongs to the same company'))
        if period_date_start > period_date_stop:
            raise osv.except_osv(_('Error'), _('Start period should be smaller then End period'))
        #for period from = january, we want to exclude the opening period (but it has same date_from, so we have to check if period_from is special or not to include that clause or not in the search).
        if period_from[0].special:
            return period_obj.search(cr, uid, [('date_start', '>=', period_date_start), ('date_stop', '<=', period_date_stop), ('company_id', '=', company1_id)])
        return period_obj.search(cr, uid, [('date_start', '>=', period_date_start), ('date_stop', '<=', period_date_stop), ('company_id', '=', company1_id), ('special', '=', False)])




    def print_template(self, cr, uid, ids, context={}):
        period_obj = self.pool.get('account.period')
        data = self.read(cr, uid, ids, [], context=context)[0]
        data_obj = self.browse(cr, uid, ids, context=context)[0]
        datas = {'periods': [], 'ids': ids}
       
        if data['period_from'] and data['period_to']:
            context['periods'] = self.build_ctx_periods(cr, uid, [data['period_from'][0]], [data['period_to'][0]])
        datas['context'] = str({'fiscalyear': data['fiscalyear'], 'periods': datas['periods'], \
                                    'state': data['target_move']})
        datas['period_from'] = data_obj.period_from.name
        datas['period_to'] = data_obj.period_to.name
        datas['fiscalyear'] = data_obj.fiscalyear.name
        context['account_fstr_root_node'] = data['root_node']
        context['hide_zero'] = data['hide_zero']
        print 'datas : ' + str(datas)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_fstr.report',
            'datas': datas,
            'context': context,
        }

    _defaults = {
        'target_move': 'posted'
    }

account_fstr_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
