# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    merchant_id = fields.Char(string="Merchant ID", config_parameter="print_service.merchant_id")
    merchant_key = fields.Char(string="Merchant Key", config_parameter="print_service.merchant_key")
