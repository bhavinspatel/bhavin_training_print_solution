#!/usr/bin/env python3
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import base64


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('print_service.group_jobworker'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            user = request.env['user.user'].sudo().search([('uid', '=', request.session.uid)])
            if user:
                return '/home'
            return '/user/data/form'
        return super(Home, self)._login_redirect(uid, redirect=redirect)


class PrintService(http.Controller):

    @http.route('/home', auth='public', type="http", csrf=False)
    def index(self):
        return request.render("print_service.customer_index")

    @http.route('/user/data/form', auth='public', type="http", csrf=False)
    def UserDataForm(self, **kw):
        user = request.env['res.users'].sudo().browse([request.session.uid])
        return request.render("print_service.user_data_form", {'user': user})

    @http.route('/user/data/create', method="post", auth='public', type="http", csrf=False)
    def UserDataCreate(self, **post):
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
                'uid': request.session.uid,
                })
        return http.local_redirect('/home')

    @http.route('/providers', auth='public', type="http", csrf=False)
    def ServiceProviderView(self, **kw):
        providers = request.env['provider.provider'].sudo().search([])
        return request.render("print_service.service_providers_view", {'providers': providers})

    @http.route('/inquiry/form/<int:provider_id>', auth='public', type="http", csrf=False)
    def InquiryForm(self, provider_id=None, **kw):
        if provider_id:
            provider = request.env['provider.provider'].sudo().search([('id', '=', provider_id)])
            object_data = request.env['object.object'].sudo().search([])
        return request.render("print_service.inquiry_form", {'provider': provider, 'object': object_data})

    @http.route('/inquiry', auth='public', type="http", csrf=False)
    def InquiryData(self, **kw):
        inquires = request.env['inquiry.inquiry'].sudo().search([('create_uid', '=', request.session.uid), ('boolean_state', '=', True)], order='id desc')
        return request.render("print_service.inquiry_data", {'inquires': inquires})

    @http.route('/inquiry/remove/<int:inquiry_id>', auth='public', type="http", csrf=False)
    def InquiryDataRemove(self, inquiry_id=None, **kw):
        if inquiry_id:
            request.env['inquiry.inquiry'].sudo().browse([inquiry_id]).unlink()
        return http.local_redirect('/inquiry')

    @http.route('/inquiry/store/<int:provider_id>', auth='public', method="post", type="http", csrf=False)
    def InquiryStore(self, provider_id=None, **post):
        if post:
            file_name = post.get('attachment')
            file = '/home/bhav/Pictures/' + file_name
            file = open(file, "rb")
            request.env['inquiry.inquiry'].sudo().create({
                'name': post.get('name'),
                'object_id': post.get('object'),
                'cust_id': request.env['user.user'].sudo().search([('uid', '=', request.session.uid)], limit="1"),
                'provider_id': provider_id,
                'attachment': base64.encodestring(file.read()),
                'location': post.get('delivery_location'),
                'remark': post.get('remark')
                })
        return http.local_redirect('/inquiry')

    @http.route('/order', auth='public', type="http", csrf=False)
    def OrderData(self, **kw):
        orders = request.env['order.order'].sudo().search([('create_uid', '=', request.session.uid)])
        return request.render("print_service.order_data", {'orders': orders})
