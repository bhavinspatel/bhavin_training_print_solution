from odoo import http
from odoo.http import request
import base64

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

	@http.route('/image', auth="public", website=True, csrf=False)
	def printImage(self):
		images = request.env['print.image'].search([])
		return request.render('bhavin_training_print_solution.print_image', {'images' : images})

	@http.route(['/image/store', '/image/delete/<model("print.image"):remove_image>'], auth="public", method="post", website=True, csrf=False)
	def printStoreImage(self, remove_image=None, **post):
		if remove_image:
			remove_image.unlink()
			return request.redirect('/image')
		file = []
		if post:
			file_name = post.get('image')
			image_file = '../Pictures/' + file_name
			if image_file == '../Pictures/' or '../Pictures/' not in image_file:
				return request.redirect('/image')
			img = open(image_file, "rb")
			request.env['print.image'].create({'image' : base64.encodestring(img.read())})
		return request.redirect('/image')