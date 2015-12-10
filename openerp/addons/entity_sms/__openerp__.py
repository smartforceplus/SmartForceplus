{
    'name': "Entity SMS",
    'version': "2.9.7.1",
    'author': "Sythil",
    'category': "Tools",
    'summary': "Allows 2 way sms conversations between leads/partners using the twilio gateway",
    'data': [
        'ir.cron.csv',
        'esms_core.xml',
        'res_partner.xml',
        'esms_history.xml',
        'esms_accounts.xml',
        'esms_templates.xml',
        'esms_import.xml',
        'esms_compose.xml',
        'esms_mass_sms.xml',
        'esms_compose_multi.xml',
        'esms_autoresponse.xml',
        'esms_verified_numbers.xml',
        'esms.gateways.csv',
	'security/ir.model.access.csv',
	'res.country.csv',
	'smsgateway/gateway_config.xml',
        'smsglobal/gateway_config.xml',
        'twilio/gateway_config.xml',
        'ir_actions.xml',
        'esms_settings.xml',
    ],
    'demo': [],
    'depends': ['web', 'crm','marketing'],
    'images':[
    'static/description/2.jpg',
    'static/description/1.png',
    'static/description/3.png',
    'static/description/4.png',
    'static/description/5.png',
    'static/description/6.png',
    'static/description/7.png',
    'static/description/10.png',
    'static/description/11.png',
    'static/description/12.png',
    ],
    'installable': True,
}