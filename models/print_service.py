# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import uuid
from odoo import models, fields, api


class PrintUser(models.Model):
    _name = 'print.user'
    _description = 'Print User Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="User Name", required=True)
    address = fields.Char(string="Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Integer(string="Pincode", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    email = fields.Char(string="Email", required=True)
    uid = fields.Many2one(string="User ID", comodel_name="res.users")


class PrintProvider(models.Model):
    _name = 'print.service.provider'
    _description = 'Print Provider Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    owner_name = fields.Char(string="Owner Name", required=True)
    name = fields.Char(string="Shop Name", required=True)
    shop_image = fields.Binary(string="Shop Image", attachment=True)
    gst_number = fields.Char(string="GST Number", required=True)
    address = fields.Char(string="Address", required=True)
    city = fields.Char(string="City", required=True)
    district = fields.Char(string="District", required=True)
    state = fields.Char(string="State", required=True)
    pincode = fields.Integer(string="Pincode", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    email = fields.Char(string="Email", required=True)
    open_time = fields.Char(string="Opening Time", required=True)
    closed_time = fields.Char(string="Closing Time", required=True)
    uid = fields.Many2one(string="User ID", comodel_name="res.users")


class PrintObject(models.Model):
    _name = 'print.object'
    _description = 'Print Object Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Object Name", required=True)
    object_type = fields.Char(string="Object Type", required=True)


class PrintInquiry(models.Model):
    _name = 'print.inquiry'
    _description = 'Print Inquiry Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Inquiry Name", required=True)
    object_id = fields.Many2one(string="Print Object", comodel_name="print.object", required=True)
    cust_id = fields.Many2one(string="User Name", comodel_name="print.user", required=True)
    attachment = fields.Binary(string="File", attachment=True)
    provider_id = fields.Many2one(string="Provider Name", comodel_name="print.service.provider", required=True)
    location = fields.Char(string="Delivery Location", required=True)
    remark = fields.Char(string="Remark")
    active = fields.Boolean(default=True)

    def inquiry_accept(self):
        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'print.order',
                'target': 'current',
                'res_id': False,
                'type': 'ir.actions.act_window',
                'context': {'inquiry_id': self.id}
                }


class PrintOrder(models.Model):
    _name = 'print.order'
    _description = 'Print Order Details'
    _rec_name = 'inquiry_id'

    def _default_order_reference(self):
        return str(uuid.uuid4())

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    start = fields.Datetime(string="Start Printing")
    end = fields.Datetime(string="End Printing")
    amount = fields.Float(string="Amount")
    state = fields.Selection([('pending', 'Pending'), ('progress', 'In Progress'), ('complated', 'Complated'), ('dispatched', 'Dispatched'),
                            ('delivered', 'Delivered')], string="Status", default=None)
    inquiry_id = fields.Many2one(string="Inquiry Name", comodel_name="print.inquiry", required=True)
    object_id = fields.Many2one(string="Print Object", comodel_name="print.object", related="inquiry_id.object_id", store=True)
    cust_id = fields.Many2one(string="Customer Name", comodel_name="print.user", related="inquiry_id.cust_id", store=True)
    location = fields.Char(string="Delivery Location", related="inquiry_id.location")
    attachment = fields.Binary(string="File", related="inquiry_id.attachment")
    provider_id = fields.Many2one(string="Provider Name", related="inquiry_id.provider_id")
    remark = fields.Char(string="Remark", related="inquiry_id.remark")
    order_reference = fields.Char(default=_default_order_reference, store=True)
    acquirer_ref = fields.Char(string="Transaction ID")
    payment_date = fields.Datetime(string="Payment Date")
    payment_status = fields.Selection([('pending', 'Pending'), ('failed', 'Failed'), ('success', 'Success')], string="Payment Status", default='pending')
    active = fields.Boolean(default=True)

    def action_pending(self):
        self.write({'state': 'pending'})

    def action_progress(self):
        self.write({'state': 'progress'})

    def action_complated(self):
        self.write({'state': 'complated'})

    def action_dispatched(self):
        self.write({'state': 'dispatched'})

    def action_delivered(self):
        self.write({'state': 'delivered'})

    @api.onchange('inquiry_id')
    def _onchange_getData(self):
        if self.env.context.get('inquiry_id'):
            self.inquiry_id = self.env.context.get('inquiry_id')

    @api.model
    def create(self, vals):
        self.env['print.inquiry'].browse([vals.get('inquiry_id')]).write({'active': False})
        return super(PrintOrder, self).create(vals)
