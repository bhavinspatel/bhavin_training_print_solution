#!/usr/bin/env python3
from odoo import models, fields, api


class User(models.Model):
    _name = 'user.user'
    _description = 'User Details'

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


class Provider(models.Model):
    _name = 'provider.provider'
    _description = 'Provider Details'

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


class Object(models.Model):
    _name = 'object.object'
    _description = 'Object Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Object Name", required=True)
    object_type = fields.Char(string="Object Type", required=True)


class Inquiry(models.Model):
    _name = 'inquiry.inquiry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inquiry Details'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Inquiry Name", required=True)
    object_id = fields.Many2one(string="Print Object", comodel_name="object.object", required=True)
    cust_id = fields.Many2one(string="User Name", comodel_name="user.user", required=True)
    attachment = fields.Binary(string="File", attachment=True)
    provider_id = fields.Many2one(string="Provider Name", comodel_name="provider.provider", required=True)
    location = fields.Char(string="Delivery Location", required=True)
    remark = fields.Char(string="Remark")
    boolean_state = fields.Boolean(required=True, default=True)

    def inquiry_accept(self):
        return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'order.order',
                    'target': 'current',
                    'res_id': False,
                    'type': 'ir.actions.act_window',
                    'context': {'inquiry_id': self.id}
                }


class Order(models.Model):
    _name = 'order.order'
    _description = 'Order Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'inquiry_id'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    start = fields.Datetime(string="Start Printing")
    end = fields.Datetime(string="End Printing")
    price = fields.Float(string="Price")
    state = fields.Selection([('pending', 'Pending'), ('progress', 'In Progress'), ('complated', 'Complated'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered')], string="Status", default="pending")
    inquiry_id = fields.Many2one(string="Inquiry Name", comodel_name="inquiry.inquiry", required=True)
    object_id = fields.Many2one(string="Print Object", comodel_name="object.object", related="inquiry_id.object_id", store=True)
    cust_id = fields.Many2one(string="Customer Name", comodel_name="user.user", related="inquiry_id.cust_id")
    location = fields.Char(string="Delivery Location", related="inquiry_id.location")
    attachment = fields.Binary(string="File", related="inquiry_id.attachment")
    provider_id = fields.Many2one(string="Provider Name", related="inquiry_id.provider_id")
    remark = fields.Char(string="Remark", related="inquiry_id.remark")

    def action_pending(self):
        self.write({'state': 'pending'})
        return True

    def action_progress(self):
        self.write({'state': 'progress'})
        return True

    def action_complated(self):
        self.write({'state': 'complated'})
        return True

    def action_dispatched(self):
        self.write({'state': 'dispatched'})
        return True

    def action_delivered(self):
        self.write({'state': 'delivered'})
        return True

    @api.onchange('inquiry_id')
    def getData(self):
        if self.env.context.get('inquiry_id'):
            self.inquiry_id = self.env.context.get('inquiry_id')

    @api.model
    def create(self, vals):
        self.env['inquiry.inquiry'].browse([vals.get('inquiry_id')]).write({'boolean_state': False})
        return super(Order, self).create(vals)
