# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('print_service.group_jobworker'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            if request.env['user.user'].sudo().search([('uid', '=', request.session.uid)]):
                return '/home'
            return '/user/data/form'
        return super(Home, self)._login_redirect(uid, redirect=redirect)


class PrintService(http.Controller):

    @http.route('/home', auth='user', type="http")
    def index(self):
        return request.render("print_service.portal_customer_index")

    @http.route('/user/data/form', auth='user', type="http")
    def user_data_form(self, **kw):
        return request.render("print_service.portal_user_data_form", {'user': request.env['res.users'].sudo().browse([request.session.uid])})

    @http.route('/user/data/create', methods=['POST'], auth='user', type="http", csrf=False)
    def user_data_create(self, **post):
        if post:
            request.env['user.user'].sudo().create({
                'name': post.get('name'),
                'address': post.get('address'),
                'city': post.get('city'),
                'district': post.get('district'),
                'state': post.get('state'),
                'pincode': post.get('pincode'),
                'mobile': post.get('mobile'),
                'email': post.get('email'),
                'uid': request.session.uid
                })
        return http.local_redirect('/home')

    @http.route('/providers', auth='user', type="http")
    def service_provider_view(self, **kw):
        return request.render("print_service.portal_service_providers_view", {'providers': request.env['provider.provider'].sudo().search([])})

    @http.route('/inquiry/form/<model("provider.provider"):provider>', auth='user', type="http")
    def inquiry_form(self, provider=None, **kw):
        return request.render("print_service.portal_inquiry_form", {'provider': provider, 'object': request.env['object.object'].sudo().search([])})

    @http.route('/inquiry', auth='user', type="http")
    def inquiry_data(self, **kw):
        return request.render("print_service.portal_inquiry_data_view", {'inquires': request.env['inquiry.inquiry'].sudo().search([('create_uid', '=', request.session.uid), ('active', '=', True)], order='id desc')})

    @http.route('/inquiry/remove/<model("inquiry.inquiry"):inquiry>', auth='user', type="http")
    def inquiry_data_remove(self, inquiry=None, **kw):
        if inquiry:
            inquiry.unlink()
        return http.local_redirect('/inquiry')

    @http.route('/inquiry/store/<model("provider.provider"):provider>', auth='user', methods=['POST'], type="http", csrf=False)
    def inquiry_store(self, provider=None, **post):
        if post:
            file = '/home/bhav/Pictures/' + post.get('attachment')
            file = open(file, "rb")
            request.env['inquiry.inquiry'].sudo().create({
                'name': post.get('name'),
                'object_id': post.get('object'),
                'cust_id': request.session.uid,
                'provider_id': provider.id,
                'attachment': base64.encodestring(file.read()),
                'location': post.get('delivery_location'),
                'remark': post.get('remark')
                })
        return http.local_redirect('/inquiry')

    @http.route('/order', auth='user', type="http")
    def order_data(self, **kw):
        return request.render("print_service.portal_order_data_view", {'orders': request.env['order.order'].sudo().search([('create_uid', '=', request.session.uid)])})
