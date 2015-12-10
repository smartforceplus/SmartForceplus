{
    'name': "Daily Unpaid Invoices(TAGSBM)",
    'version': "1.0",
    'author': "TAGSBM",
    'category': "Tools",
    'summary': "Emails a daily report of all unpaid invoices",
    'data': [
        'email.template.csv',
        'ir.cron.csv',
    ],
    'demo': [],
    'depends': ['web', 'account','report'],
    'installable': True,
}