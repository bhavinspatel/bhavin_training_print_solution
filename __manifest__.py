# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Print Service',
    'summary': 'This is a Print service Application',
    'description': 'This Application Provide online printing and couriar services',
    'author': 'Bhavin Patel',
    'depends': ['web_dashboard', 'portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/web_templates.xml',
        'views/registration_templates.xml',
        'views/portal_views.xml',
    ],
    'application': True
}
