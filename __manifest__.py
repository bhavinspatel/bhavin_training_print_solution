{
    'name': 'Print Service',
    'summary': 'This is a Print service Application',
    'description': 'This Application Provide online printing and couriar services',
    'author': 'Bhavin Patel',
    'version': '0.1',
    'depends': ['base', 'web_dashboard', 'portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/main_template.xml',
        'views/registration_template.xml',
        'views/customer_template.xml',
    ],
    'demo': [
    ],
    'application': True
}
