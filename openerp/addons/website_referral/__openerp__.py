{
    'name': 'TAG Referral Form',
    'category': 'Website',
    'website': 'https://www.odoo.com/page/website-builder',
    'summary': 'Modified Origional Contact Us Form to create a second custom that adds referrals',
    'version': '1.0',
    'description': """
OpenERP Contact Form
====================

        """,
    'author': 'OpenERP SA and TAG',
    'depends': ['website_partner', 'crm'],
    'data': [
        'data/website_crmref_data.xml',
		'views/website_crmref.xml',
        
    ],
    'installable': True,
    'auto_install': False,
}
