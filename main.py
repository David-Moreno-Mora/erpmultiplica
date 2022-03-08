from typing import Optional

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