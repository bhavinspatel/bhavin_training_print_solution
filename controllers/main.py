from odoo import http
from odoo.http import request

class PrintSolution(http.Controller):

	@http.route('/quotation/list/', auth='public', website=True, csrf=False)
	def quotationList(self):
		quotations = request.env['quotation.quotation'].search([])
		return request.render('bhavin_training_print_solution.quotation_list', {'quotations' : quotations})

	@http.route('/quotation/delete/<model("quotation.quotation"):quotation>', auth="public", website=True, csrf=False)
	def deleteQuotation(self, quotation=None):
		if quotation:
			quotation.unlink()
		return request.redirect('/quotation/list/')

	@http.route(['/quotation/edit/<model("quotation.quotation"):quotation>', '/quotation/new'], auth="public", website=True, csrf=False)
	def createEditQuotationForm(self, quotation=None):
		if quotation:
			quotation = request.env['quotation.quotation'].browse([quotation.id])
		return request.render('bhavin_training_print_solution.create_and_edit_quotation', {'quotation' : quotation})

	@http.route(['/quotation/data/', '/quotation/data/<int:quotation>'], method="post", auth="public", website=True, csrf=False)
	def createEditQuotation(self, quotation=None, **post):
		if post:
			if quotation:
				request.env['quotation.quotation'].browse([quotation]).write(post)
			else:
				request.env['quotation.quotation'].create(post)
		return request.redirect('/quotation/list/')