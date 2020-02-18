# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request


class PrintServiceRegistration(http.Controller):

    @http.route('/reg/form/', auth='public', csrf=False)
    def registration_form(self):
        return request.render('print_service.registration_form', {'currencys': http.request.env['res.currency'].sudo().search([])})

    @http.route('/reg/add/<string:user_type>', methods=["POST"], auth='public', csrf=False)
    def registration(self, user_type=None, **post):
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email')
            })
        if user_type == "service_provider":
            currency = request.env['res.currency'].sudo().search([('name', '=', post.get('currency'))], limit=1)
            company = request.env['res.company'].sudo().create({
                'name': post.get('shop_name'),
                'partner_id': partner.id,
                'currency_id': currency.id
                })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('password'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('print_service.print_service_group_service_providers').id])]
                })
        else:
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('password'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
                })
        return http.local_redirect('/web/login')
