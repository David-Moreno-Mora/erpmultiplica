from typing import Optional
import xmlrpc.client

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class Invoice(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/items/")
async def create_item(invoice: Invoice):
    invoice_dict = invoice.dict()
    if invoice.tax:
        price_with_tax = invoice.price + invoice.tax
        invoice_dict.update({"price_with_tax": price_with_tax})
    return invoice_dict

@app.get("/items/test/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

@app.post("/invoice")
def create_invoice():
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
    return{"id":info}