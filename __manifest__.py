{
	'name' : 'Print Solution',
	'summary' : 'This is a Print service Application',
	'description' : 'This Application Provide online printing services and couriar services',
	'author' : 'Bhavin Patel',
	'version' : '0.1',
	'depends' : ['base'],
	'data' : [
		'security/ir.model.access.csv',
		'data/data.xml',
		'wizard/provider_wizard.xml',
		'report/report.xml',
		'views/main_template.xml'
	],
	'demo' : [
	],
	'application': True
}