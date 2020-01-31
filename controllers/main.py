from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home

class Home(Home):

	def _login_redirect(self, uid, redirect=None):
		if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('print_service.group_jobworker'):
			return '/web/'
		if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
			return '/web/'
		if  request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
			return '/home'
		return super(PrintService, self)._login_redirect(uid, redirect=redirect)

class PrintService(http.Controller):

	@http.route('/home', auth='public', type="http", csrf=False)
	def index(self, **kw):
		printers = request.env['provider.provider'].sudo().search([])
		return request.render("print_service.customer_index", {'printers' : printers})