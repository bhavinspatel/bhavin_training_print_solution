{
	'name' : 'Print Solution',
	'summary' : 'This is a Print service Application',
	'description' : 'This Application Provide online printing services and couriar services',
	'author' : 'Bhavin Patel',
	'version' : '0.1',
	'depends' : ['base'],
	'data' : [
		'security/ir.model.access.csv',
		'views/main_template.xml'
	],
	'demo' : [
		'data/demo.xml'
	],
	'application' : True
}