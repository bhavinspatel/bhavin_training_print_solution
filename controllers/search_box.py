# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request


class SearchBox(http.Controller):

    @http.route('/search', auth='public', csrf=False)
    def search_box(self):
        return request.render('print_service.search_box', {'products': http.request.env['product.product'].sudo().search([])})
