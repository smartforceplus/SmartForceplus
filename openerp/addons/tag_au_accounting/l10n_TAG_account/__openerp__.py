
{
    'name': 'Australian OpenERP Chart of Accounts',
    'version': '1.0',
    'category': 'Localisation/Account Charts',
    'description': """Localisation module for UK based companies.
Recommended for SME businesses - categorised as Small to Medium Sized Enterprise (SME) 1-250 employees.  
Contains: list of 4 digit accounts, chart of accounts, account types, UK tax codes.""",
    'author': 'Emipro Technologies',
    'website': 'www.emiprotechnologies.com',
    'depends': ['base_iban', 'base_vat', 'account_chart'],
    'init_xml': [],
    'update_xml': [
        'data/account.account.type.csv',
        'data/account.account.template.csv',
        'data/account.tax.code.template.csv',
        'data/account.chart.template.csv',
        'data/account.tax.template.csv',
        'l10n_aus_tag_wizard.xml',
    ],
    'demo_xml': [],
    'installable': 'True'
}

