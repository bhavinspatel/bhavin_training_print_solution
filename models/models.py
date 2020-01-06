from odoo import models, fields, api
from odoo.exceptions import ValidationError

class User(models.Model):
	_name = 'user.user'
	_description = 'User List'

	name = fields.Char(string="User Name", required=True)
	address = fields.Char(string="Address", required=True)
	city = fields.Char(string="City", required=True)
	district = fields.Char(string="District", required=True)
	pincode = fields.Integer(string="Pincode", required=True)
	mobile = fields.Char(string="Mobile", required=True)
	email = fields.Char(string="Email", required=True)

	_sql_constraints = [
		('user_mobile_unique',
		 'UNIQUE(mobile)',
		 "The mobile number already exist."),
		('user_email_unique',
		 'UNIQUE(email)',
		 "The email id already exist."),
	]

	@api.constrains('mobile')
	def _compute_mobile(self):
		for data in self:
			if data.mobile and len(str(data.mobile)) != 10:
				raise ValidationError("Fields mobile number must be 10 digit.")
			
			if data.pincode and len(str(data.pincode)) != 6:
				raise ValidationError("Fields pincode must be 6 digit.")


class Provider(models.Model):
	_name = 'provider.provider'
	_description = 'Provider List'

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
	service_ids = fields.One2many(comodel_name="service.service", String="Services", inverse_name="provider_id")

	_sql_constraints = [
		('provider_mobile_unique',
		 'UNIQUE(mobile)',
		 "The mobile number already exist."),
		('provider_email_unique',
		 'UNIQUE(email)',
		 "The email id already exist."),
	]

	@api.constrains('mobile', 'pincode')
	def _compute_mobile(self):
		for data in self:
			if data.mobile and len(str(data.mobile)) != 10:
				raise ValidationError("Fields mobile number must be 10 digit.")
			
			if data.pincode and len(str(data.pincode)) != 6:
				raise ValidationError("Fields pincode must be 6 digit.")

	def unlink(self):
		s_id = self.mapped('service_ids')
		if s_id:
			s_id.unlink()
		return super(Provider, self).unlink()

class Services(models.Model):
	_name = 'service.service'
	_description = 'Services List'

	provider_id = fields.Many2one(comodel_name="provider.provider", string="Shop Name", required=True)
	page_type = fields.Selection([('A0 Page', 'A0 Page'), ('A1 Page', 'A1 Page'),
									('A2 Page', 'A2 Page'), ('A3 Page', 'A3 Page'),
									('A4 Page', 'A4 Page'), ('A5 Page', 'A5 Page'),
									('A6 Page', 'A6 Page'), ('Flex Benner', 'Flex Benner'),
									('Visiting Card', 'Visiting Card')], 
									string="Page Type", required=True)
	printing_type = fields.Selection([('Black-White', 'Black-White'), ('Color', 'Color')], string="Printing Type", required=True)
	description = fields.Char(string="Description", required=True)
	price = fields.Float(string="Price", required=True)