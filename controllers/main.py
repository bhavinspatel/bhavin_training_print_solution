from odoo import http
from odoo.http import request

class PrintSolution(http.Controller):

	@http.route('/quotation/list/', auth='public', website=True, csrf=False)
	def quotationList(self):
		quotations = request.env['quotation.quotation'].search([])
		return request.render('bhavin_training_print_solution.quotation_list', {'quotations' : quotations})

	@http.route('/quotation/delete/<model("quotation.quotation"):quotation>', auth="public", website=True, csrf=True)
	def deleteQuotation(self, quotation=None):
		if quotation:
			quotation.unlink()
		return request.redirect('/quotation/list/')

	@http.route(['/quotation/edit/<model("quotation.quotation"):quotation>', '/quotation/new'], auth="public", website=True, csrf=True)
	def createEditQuotationForm(self, quotation=None):
		if quotation:
			print(quotation)
			print(quotation.id)
			quotation = request.env['quotation.quotation'].browse([quotation.id])
		print('Yoooooooooooooooooo')
		return request.render('bhavin_training_print_solution.create_and_edit_quotation', {'quotation' : quotation})

	@http.route('/quotation/data/<model("quotation.quotation"):quotation>', method="post", auth="public", website=True, csrf=True)
	def createQuotation(self, quotation=None, **post):
		if post:
			request.env['quotation.quotation'].browse([quotation])
		return request.redirect('/quotation/list/')