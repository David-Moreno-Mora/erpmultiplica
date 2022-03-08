import xmlrpc.client

url = 'https://marcomoramultiplica-erp.odoo.com'
db = 'marcomoramultiplica-erp-prod-4175354'
username = 'admin'
password = '2c51131e4bccac3a42bbf4767f00374d9900ae23'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
items = {
    'product_id': 1,
    'quantity': 10,
    'price_unit': 30,
}
invoice = {
    "move_type":"out_invoice",
    "currency_id":33,
    "journal_id":1,
    "state":"draft",
    "company_id":1,
    'invoice_line_ids': [(0, 0, items)],
}
info = models.execute_kw(db, uid, password,'account.move','create',[invoice])
print(info)