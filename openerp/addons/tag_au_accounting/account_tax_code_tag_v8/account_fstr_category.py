# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)
#    2010 Colin MacMillan - Publicus Solutions Ltd.
#    All Rights Reserved
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
import openerp.addons.decimal_precision as dp
from wizard import account_fstr_wizard

class account_fstr_tax_code_category(osv.osv):
    _name = "account_fstr_tax_code.category"
    _description = "Financial Statement template category"
    _order = "sequence, id"


    def __compute(self, cr, uid, ids, field_names, arg=None, context=None,
                  query='', query_params=()):
        res = {}
        for category_obj in  self.browse(cr, uid, ids, context=context):
            res.update({category_obj.id: self.__compute_balance_for_caregory(cr, uid, category_obj, context=context)})
        return res

    def __compute_balance_for_caregory(self, cr, uid, category_obj, context={}):
        result = 0
        if category_obj.state == 'normal':
            for tax_code_obj in category_obj.tax_code_ids:
                result += round(tax_code_obj.sum,0) * tax_code_obj.sign
        else:
            for child_category_obj in category_obj.child_id:
                result += self.__compute_balance_for_caregory(cr, uid, child_category_obj, context=context)
        return result


    _columns = {
        'name': fields.char('Category Title name', size=128, required=True,),
        'digits_round': fields.integer('Digits round', required=True),
        'company_id': fields.many2one('res.company', 'Company', ondelete='set null'),
        'name_end': fields.char('Category End/Total name', size=128,),
        'display_total': fields.boolean('Display End/Total'),
        'progenitor_id': fields.integer('Progenitor id'),
        'progenitor_name': fields.char('Progenitor', size=128),
        'parent_id': fields.many2one('account_fstr_tax_code.category', 'Parent node', ondelete='cascade'),
        'sequence': fields.integer('Sequence'),
        'consolidate_total': fields.boolean('Consolidate total', help="Selecting Consolidate total will print this category total as a single summed figure and will not list out each individual account"),
        'display_heading': fields.boolean('Display title'),

        'bold_title': fields.boolean('Bold'),
        'italic_title': fields.boolean('Italic'),
        'underline_title': fields.boolean('Unnderline'),

        'bold_end': fields.boolean('Bold'),
        'italic_end': fields.boolean('Italic'),
        'underline_end': fields.boolean('Unnderline'),

        'inversed_sign': fields.boolean('Inversed sign'),
        'child_id': fields.one2many('account_fstr_tax_code.category', 'parent_id', 'Consolidated Children'),
        'tax_code_ids': fields.many2many('account.tax.code', 'account_fstr_category_account_tax_code', 'tax_id', 'category_id', 'Tax Codes'),
        'indent_title': fields.integer('Indent Title, (pt)'),
        'indent_end': fields.integer('Indent End, (pt)'),
        'top_spacing_title': fields.integer('Top spacing Title, (pt)'),
        'top_spacing_end': fields.integer('Top spacing End, (pt)'),
        'bottom_spacing_title': fields.integer('Bottom spacing Title, (pt)'),
        'bottom_spacing_end': fields.integer('Bottom spacing End, (pt)'),
        'state': fields.selection([('view','View'),('root','Root'),('normal','Normal')], 'Type'),
        'balance': fields.function(__compute, digits_compute=dp.get_precision('Account'), method=True, string='Balance', store=False, type='float'),        
        'printable': fields.boolean('Printable', help="Select to allow category to display in print list"),
        'operation':fields.selection([('divide','Divide By'),('multiplication','Multiply By')],'Operation'),
        'operation_value':fields.float('Value'),
    }

    _defaults = {
        'state': 'normal',
        'indent_title': 10,
        'indent_end': 10,
        'top_spacing_title': 0,
        'digits_round': 0,
    }

    def print_template(self, cr, uid, ids, context={}):
        return account_fstr_wizard.account_fstr_wizard.print_template(cr, uid, ids, context={})


    def _get_selected_accounts(self, cr, uid, progenitor_id,
                               current_category_id, context={}):
        result = []
        category_ids = self.search(cr, uid, [('progenitor_id', '=', progenitor_id)], context=context)
        for category_obj in self.browse(cr, uid, category_ids, context=context):
            if category_obj.id != current_category_id[0]:
                result.extend([category.id for category in category_obj.tax_code_ids])
        return result

    def test_account_list(self, cr, uid, ids, progenitor_id, tax_code_ids):
        warning = {}
        warning_tax_code_names = []
        current_tax_code_ids = []
        all_tax_code_ids_for_template = self._get_selected_accounts(cr, uid,
                                                                   progenitor_id,
                                                                   ids)
        updated_tax_code_ids = tax_code_ids[0][2]
        for tax_code_obj in self.pool.get('account.tax.code').browse(cr, uid, updated_tax_code_ids):
            if not (tax_code_obj.id in all_tax_code_ids_for_template):
                current_tax_code_ids.append(tax_code_obj.id)
            else:
                warning_tax_code_names.append(tax_code_obj.name)
        if warning_tax_code_names:
            warning.update({
                'title': 'Alert',
                'message': "Tax Codes %s already exist in current template" % (", ".join(warning_tax_code_names)),
            })
        return {'value': {'tax_code_ids': current_tax_code_ids,}, 'warning': warning}

account_fstr_tax_code_category()


class account_fstr_category(osv.osv):
    _name = "account_fstr_tax_code.category"
    _inherit = "account_fstr_tax_code.category"


    def _get_progenitor_id(self, cr, uid, ids, field_names, arg=None, context={}):
        res = {}
        for category_obj in self.browse(cr, uid, ids, context=context):
            res.update({category_obj.id: self._get_progenitor_id_in_recurse(cr, uid, category_obj, context=context) })
        return res

    def _get_progenitor_id_in_recurse(self, cr, uid, category_obj, context={}):
        result = {}
        if not (category_obj.parent_id and category_obj.parent_id.id):
            result = {'progenitor_id': category_obj.id, 'progenitor_name': category_obj.name}
        else:
            result = self._get_progenitor_id_in_recurse(cr, uid, category_obj.parent_id, context=context)
        return result

    def _get_childs(self, cr, uid, ids, context={}):
        return self.search(cr, uid, [('id', 'child_of', ids)], context=context)



    _columns = {
        'progenitor_id': fields.function(_get_progenitor_id, method=True, string='Progenitor', type='integer', store={ 'account_fstr_tax_code.category': (_get_childs, ['parent_id'], 1)}, multi=True),
        'progenitor_name': fields.function(_get_progenitor_id, method=True, string='Progenitor', type='char', store={ 'account_fstr_tax_code.category': (_get_childs, ['parent_id'], 1)}, multi=True),

    }

account_fstr_category()
