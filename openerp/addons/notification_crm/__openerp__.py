{
    'name': 'CRM Deadline Notifications',
    'version': '1.1',
    'category': 'Customer Relationship Management',
    'author': 'IT Libertas',
    'website': 'http://itlibertas.net/',
    'depends': ['crm'],
    'data': [
            'views/crm_view.xml',
            'data/notification_lead_data.xml'
            ],
    'update_xml': [],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'price': '10.0',
    'currency': 'USD',
    'images': ['static/description/main.png'],
    'summary': 'Daily notifications which contain list of leads/opportunities with exceeded deadline',
    'description': '''
CRM Notifications: Actions under Control
========================================
Increase conversion of sales efforts
------------------------------------
The module allows sending daily reminders about today and overpassed actions grouped by leads/opportunities. Force your sales managers to work efficiently. No forgetting, no excuses.
* Daily reminders about today and overpassed actions grouped by leads/opportunities
* Notifications are based on editable template with references for related objects
* Allow configuring notifications based on leads/opportunities stages
Useful summary to start a day
-----------------------------
Notifications are based on the editable template with references for related objects. Just click and do. Moreover, each email is individual and the language is set according to each user preferences.
Flexible configuration
----------------------
You are able to apply notifications for chosen leads/opportunities stages. Get only up-to-date and essential data.
    '''
}
