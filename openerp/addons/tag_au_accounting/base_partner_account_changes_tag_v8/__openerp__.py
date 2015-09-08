
{
    'name': 'Change partner bank account details',
    'version': '1.0',
    'category': 'Project Email Communication',
    "sequence": 14,
    'complexity': "normal",
    'description': """
    Module changes partner bank related details
    """,
    'author': 'TAG',
    'website': 'http://www.smallbiz.community',
    'images': [],
    'depends': ['base_iban'],
    'init_xml': [],
    'update_xml': [
                   'partner_bank_view_changes.xml',
                   ],
    'demo_xml': [],
    'data' : [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
