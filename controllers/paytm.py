import json
import urls
from odoo import request
from . import checksum


# add checksum file in your controller folder for now. with same given (just copy it to the controller folder)

# add two fields in your model of payment
# 1) order_id, default value for order id is -> str(uuid.uuid4())
# 2) acquirer_ref


# add this code in your paytm controller
base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
data_dict = {
    'redirection_url': "https://pguat.paytm.com/oltp-web/processTransaction",
    'MID': 'merchant_id from system param',
    'WEBSITE': 'WEBSTAGING',  # fix value
    'ORDER_ID': 'order id field from your model',
    'CUST_ID': request.uid,
    'INDUSTRY_TYPE_ID': 'Retail',  # fix value
    'CHANNEL_ID': 'WEB',  # fix value
    'TXN_AMOUNT': 'amount',
    'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
}
data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'merchant_key from system param')
return request.make_response(json.dumps(data_dict))


# credentials
# ===========
sandbox_merchant_id = 'TinyER40943268666403'  # add this in config param
website_url = 'WEBSTAGING'
sandbox_merchant_key = 'XdanaSDPoWj#!P7s'  # add this in config param
industry_type = 'Retail'
