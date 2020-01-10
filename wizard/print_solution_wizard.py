from odoo import models, fields, api

class ProviderWizard(models.TransientModel):
	_name = 'provider.wizard'
	_description = "Provider Wizard"

	def _default_provider(self):
		return self.env['provider.provider'].browse(self._context.get('active_id'))

	provider_id = fields.Many2one(comodel_name="provider.provider", string="Provider", required=True, default=_default_provider)
	page_type = fields.Selection([('A0 Page', 'A0 Page'), ('A1 Page', 'A1 Page'),
									('A2 Page', 'A2 Page'), ('A3 Page', 'A3 Page'),
									('A4 Page', 'A4 Page'), ('A5 Page', 'A5 Page'),
									('A6 Page', 'A6 Page'), ('Flex Benner', 'Flex Benner'),
									('Visiting Card', 'Visiting Card')], 
									string="Page Type", required=True)
	printing_type = fields.Selection([('Black-White', 'Black-White'), ('Color', 'Color')],
										string="Printing Type", required=True)
	description = fields.Char(string="Description", required=True)
	price = fields.Float(string="Price", required=True)