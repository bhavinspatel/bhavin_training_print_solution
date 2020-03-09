# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import json
from . import checksum
from datetime import datetime
from werkzeug import urls

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


# class Home(Home):

#     def _login_redirect(self, uid, redirect=None):
#         if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('print_service.group_jobworker'):
#             return '/web/'
#         if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
#             if request.env['print.user'].sudo().search([('uid', '=', request.session.uid)], limit=1):
#                 return '/home'
#             return '/user/data/form'
#         return super(Home, self)._login_redirect(uid, redirect=redirect)


class PrintService(http.Controller):

    @http.route('/home', auth='user', type="http")
    def index(self):
        return request.render("print_service.portal_customer_index")

    @http.route('/user/data/form', auth='user', type="http")
    def user_data_form(self, **kw):
        return request.render("print_service.portal_user_data_form", {'user': request.env['res.users'].browse([request.session.uid])})

    @http.route('/user/data/create', methods=['POST'], auth='user', type="http", csrf=False)
    def user_data_create(self, **post):
        if post:
            request.env['print.user'].create({
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
        return request.render("print_service.portal_service_providers_view", {'providers': request.env['print.service.provider'].search([])})

    @http.route('/inquiry/form/<model("print.service.provider"):provider>', auth='user', type="http")
    def inquiry_form(self, provider=None, **kw):
        return request.render("print_service.portal_inquiry_form", {'provider': provider, 'object': request.env['print.object'].search([])})

    @http.route('/inquiry', auth='user', type="http")
    def inquiry_data(self, **kw):
        return request.render("print_service.portal_inquiry_data_view", {'inquires': request.env['print.inquiry'].search([('cust_id', '=', request.env['print.user'].sudo().search([('uid', '=', request.session.uid)]).id), ('active', '=', True)], order='id desc')})

    @http.route('/inquiry/remove/<model("print.inquiry"):inquiry>', auth='user', type="http")
    def inquiry_data_remove(self, inquiry=None, **kw):
        if inquiry:
            inquiry.unlink()
        return http.local_redirect('/inquiry')

    @http.route('/inquiry/store/<model("print.service.provider"):provider>', auth='user', methods=['POST'], type="http", csrf=False)
    def inquiry_store(self, provider=None, **post):
        if post:
            file = '/home/bhav/Pictures/' + post.get('attachment')
            file = open(file, "rb")
            request.env['print.inquiry'].create({
                'name': post.get('name'),
                'object_id': post.get('object'),
                'cust_id': request.env['print.user'].sudo().search([('uid', '=', request.session.uid)], limit=1).id,
                'provider_id': provider.id,
                'attachment': base64.encodestring(file.read()),
                'location': post.get('delivery_location'),
                'remark': post.get('remark')
                })
        return http.local_redirect('/inquiry')

    @http.route('/order/payment', auth='user', type="http")
    def inquiry_payment_form(self, **kw):
        orders = request.env['print.order'].search([('cust_id', '=', request.env['print.user'].sudo().search([('uid', '=', request.session.uid)]).id), ('payment_status', '=', 'pending')])
        return request.render("print_service.portal_order_payment", {'orders': orders})

    @http.route('/order/payment/<model("print.order"):order>', auth='user', type="http")
    def payment_form(self, order=None, **kw):
        return request.render("print_service.portal_order_payment_form", {'order': order})

    @http.route('/payment', auth='user', type="http", csrf=False)
    def payment(self, **kw):
        order = request.env['print.order'].browse([int(kw.get('order_id'))])
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        data_dict = {
            'MID': 'TinyER40943268666403',
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': str(order.order_reference),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(order.amount),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'XdanaSDPoWj#!P7s')
        data_dict['redirection_url'] = 'https://securegw-stage.paytm.in/order/process'
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response', type="http", csrf=False)
    def paytm_response(self, **kw):
        print('\n\n\n', kw)
        order_payment = request.env['print.order'].search([('order_reference', '=', kw.get('ORDERID'))], limit=1)
        if checksum.verify_checksum(kw, 'XdanaSDPoWj#!P7s', kw.get('CHECKSUMHASH')):
            if(kw.get('STATUS') == 'TXN_SUCCESS'):
                date_string = kw.get('TXNDATE')
                order_payment.write({'payment_date': datetime.strptime(date_string[:-2], '%Y-%m-%d %H:%M:%S'), 'acquirer_ref': kw.get('TXNID'), 'payment_status': 'success', 'state': 'pending'})
                return request.render("print_service.portal_payment_message", {'context': kw})
            elif(kw.get('STATUS') == 'TXN_FAILURE'):
                order_payment.write({'payment_status': 'failed', 'active': False})
                return request.render("print_service.portal_payment_message", {'context': kw})
            return http.local_redirect('/order')
        else:
            return http.local_redirect("/order/payment")

    @http.route('/order', auth='user', type="http")
    def order_data(self, **kw):
        orders = request.env['print.order'].search([('cust_id', '=', request.env['print.user'].sudo().search([('uid', '=', request.session.uid)]).id), ('state', '!=', None)])
        return request.render("print_service.portal_order_data_view", {'orders': orders})
