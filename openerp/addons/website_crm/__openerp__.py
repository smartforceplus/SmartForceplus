{
    'name': 'TAG Contact Form Rev A',
    'category': 'Website',
    'website': 'https://www.odoo.com/page/website-builder',
    'summary': 'Origional Module Modified By TAG for Subdivision and Strata',
    'version': '1.0',
    'description': """
OpenERP Contact Form
====================

        """,
    'author': 'OpenERP SA and TAG',
    'depends': ['website_partner', 'crm'],
    'data': [
        'data/website_crm_data.xml',
		'views/website_crm.xml',
        
    ],
    'installable': True,
    'auto_install': False,
}
