
{
    'name': 'TAG Australian Accounting',
    'version': '1.0',
    'depends': ['account_voucher', 'account_accountant', 'base', 'base_iban', 'base_vat', 'account', 'account_chart'],
    'category': 'Localisation/Account Charts',
    'description': """Localisation module for AU based companies.
Recommended for SME businesses - categorised as Small to Medium Sized Enterprise (SME) 1-250 employees.  
Contains: list of 4 digit accounts, chart of accounts, account types, AU tax codes.""",
    'author': 'TAG Small Biz Community',
    'website': 'http://www.smallbiz.community',
    'data': [
    
                        'account_tax_code_tag_v8/security/ir.model.access.csv',
                        'account_tax_code_tag_v8/account_fstr_wizard_view.xml',
                        'account_tax_code_tag_v8/account_fstr_view.xml',
                        'account_tax_code_tag_v8/account_fstr_menu.xml',
                        'account_tax_code_tag_v8/account_tax_code_view.xml',                      
           
                   'accounts_reports_tag_v8/account_report_group.xml',
	           'accounts_reports_tag_v8/account_fstr_html_report.xml',
                   'accounts_reports_tag_v8/aged_partner_balance.xml',
                   
                            


        
                   'base_partner_account_changes_tag_v8/partner_bank_view_changes.xml',
    
                   'company_related_changes_tag_v8/field_in_company_screen.xml',
    
    
                   'decimal_precision/decimal_precision_view.xml',
                   'decimal_precision/security/ir.model.access.csv',
    
                   'invoice_open_form_view_tag_v8/invoice_line_in_new_form.xml',
    
    
                   'l10n_openerp_au/data/account.account.type.csv',
                   'l10n_openerp_au/data/account.account.template.csv',
                   'l10n_openerp_au/data/account.tax.code.template.csv',
                   'l10n_openerp_au/data/account.chart.template.csv',
                   'l10n_openerp_au/data/account.tax.template.csv',
    #        'l10n_openerp_au/data/account_tax_code.xml',
    #        'l10n_openerp_au/data/account_tax.xml',
                   'l10n_openerp_au/l10n_au_wizard.xml',
                   'l10n_openerp_au/data/res.country.state.csv',
        
        
                   'l10n_TAG_account/data/account.account.type.csv',
                   'l10n_TAG_account/data/account.account.template.csv',
                   'l10n_TAG_account/data/account.tax.code.template.csv',
                   'l10n_TAG_account/data/account.chart.template.csv',
                   'l10n_TAG_account/data/account.tax.template.csv',
                   'l10n_TAG_account/l10n_aus_tag_wizard.xml',    
                   
                   
                   

                    'account_fstr/security/ir.model.access.csv',
                    'account_fstr/account_fstr_wizard_view.xml',
                    'account_fstr/account_fstr_view.xml',
                    'account_fstr/account_fstr_menu.xml'    
                     
    
    ],
    'installable': 'True'
}

