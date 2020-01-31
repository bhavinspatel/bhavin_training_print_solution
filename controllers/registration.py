from odoo import http
from odoo.http import request

class PrintServiceRegistration(http.Controller):

	@http.route('/reg/form/', auth='public', csrf=False)
	def registration_form(self):
		currencys = http.request.env['res.currency'].sudo().search([])
		return request.render('print_service.registration_form', {'currencys' : currencys })

	@http.route('/reg/add/<string:user_type>', method="POST", auth='public', csrf=False)
	def registration(self, user_type=None, **post):
		if user_type == "service_provider":
			groups_id_name = [(6, 0, [request.env.ref('print_service.group_jobworker').id])]
			currency_name = post.get('currency')
			currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
			partner = request.env['res.partner'].sudo().create({
				'name': post.get('name'),
				'email': post.get('email')
				})
			company = request.env['res.company'].sudo().create({
				'name': post.get('shop_name'),
				'partner_id': partner.id,
				'currency_id': currency.id,
				})
			request.env['res.users'].sudo().create({
				'partner_id': partner.id,
				'login': post.get('name'),
				'password': post.get('password'),
				'company_id': company.id,
				'company_ids': [(4, company.id)],
				'groups_id': groups_id_name,
				})
		else:
			groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
			partner = request.env['res.partner'].sudo().create({
				'name': post.get('name'),
				'email': post.get('email')
				})
			request.env['res.users'].sudo().create({
				'partner_id': partner.id,
				'login': post.get('name'),
				'password': post.get('password'),
				'groups_id': groups_id_name,
				})
		return http.local_redirect('/web/login')