
{
    'name': 'Schedule report of Profit & Loss and Balance Sheet',
    'version': '1.0',
    'category': 'Customise Server Action',
    "sequence": 14,
    'complexity': "easy",
    'description': """
    Schedule Print of account reports 
    """,
    'author': 'Emipro Technologies',
    'website': 'http://www.emiprotechnologies.com',
    'images': [],
    'depends': ['account_fstr'],
    'init_xml': [],
    'update_xml': [
                   'account_report_group.xml',
                   'account_fstr_html_report.xml',
                   'aged_partner_balance.xml',
                   ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
