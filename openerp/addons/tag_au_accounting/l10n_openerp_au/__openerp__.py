# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    (C)UK OpenERP Alliance.                            
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'AU OpenERP Alliance Chart of Accounts',
    'version': '1.0',
    'category': 'Localisation/Account Charts',
    'description': """Localisation module for AU based companies.
Recommended for SME businesses - categorised as Small to Medium Sized Enterprise (SME) 1-250 employees.  
Contains: list of 4 digit accounts, chart of accounts, account types, AU tax codes.""",
    'author': 'AU OpenERP',
    'website': 'https://launchpad.net/~uk-openerp-alliance',
    'depends': ['base_iban', 'base_vat', 'account_chart'],
    'init_xml': ['data/account.account.type.csv',
        'data/account.account.template.csv',
        'data/account.tax.code.template.csv',
        'data/account.chart.template.csv',
        'data/account.tax.template.csv',
#        'data/account_tax_code.xml',
#        'data/account_tax.xml',
        'l10n_au_wizard.xml',
        'data/res.country.state.csv'],
    'update_xml': [        
    ],
    'demo_xml': [],
    'installable': 'True'
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
