from odoo import models, fields, api


class User(models.Model):
	_name = 'user.user'
	_description = 'User Details'

	name = fields.Char(string="User Name", required=True)
	address = fields.Char(string="Address", required=True)
	city = fields.Char(string="City", required=True)
	district = fields.Char(string="District", required=True)
	pincode = fields.Integer(string="Pincode", required=True)
	mobile = fields.Char(string="Mobile", required=True)
	email = fields.Char(string="Email", required=True)


class Provider(models.Model):
	_name = 'provider.provider'
	_description = 'Provider Details'

	owner_name = fields.Char(string="Owner Name", required=True)
	name = fields.Char(string="Shop Name", required=True)
	gst_number = fields.Char(string="GST Number", required=True)
	address = fields.Char(string="Address", required=True)
	city = fields.Char(string="City", required=True)
	district = fields.Char(string="District", required=True)
	pincode = fields.Integer(string="Pincode", required=True)
	mobile = fields.Char(string="Mobile", required=True)
	email = fields.Char(string="Email", required=True)
	open_time = fields.Char(string="Opening Time", required=True)
	closed_time = fields.Char(string="Closing Time", required=True)


class Object(models.Model):
	_name = 'object.object'
	_description = 'Object Details'

	name = fields.Char(string="Object Name", required=True)
	object_type = fields.Char(string="Object Type", required=True)


class Inquiry(models.Model):
	_name = 'inquiry.inquiry'
	_description = 'Inquiry Details'

	object_id = fields.Many2one(string="Print Object", comodel_name="object.object", required=True)
	attachment = fields.Binary(string="File", required=True)
	provider_id = fields.Many2one(string="Provider Name", comodel_name="provider.provider", required=True)
	location = fields.Char(string="Delivery Location", required=True)
	remark = fields.Char(string="Remark")


class JobWork(models.Model):
	_name = 'jobwork.jobwork'
	_description = 'JobWork Details'

	inquiry_id = fields.Many2one(string="Inquiry Name", comodel_name="inquiry.inquiry", required=True)
	start = fields.Datetime(string="Start Printing", required=True)
	end = fields.Datetime(string="End Printing", required=True)
	price = fields.Float(string="Price", required=True)
	customer_id = fields.Many2one(string="Customer Name", comodel_name="user.user", required=True)
	location = fields.Char(string="Delivery Location", related="inquiry_id.location")
	attachment = fields.Binary(string="File", related="inquiry_id.attachment")
	provider_id = fields.Many2one(string="Provider Name", related="inquiry_id.provider_id")
	remark = fields.Char(string="Remark", related="inquiry_id.remark")

