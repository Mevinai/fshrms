
from typing import List
from pydantic import BaseModel

class ItemPriceSchema(BaseModel):
    price_list:str= "Standard Selling"
    price_list_rate:float

class ItemCreateSchema(BaseModel):
    item_code: str 
    item_name:str 
    item_group:str="Products"
    stock_uom:str="Nos"
    is_stock_item: int=1
    standard_rate: float
    item_tax_template:str="VAT 15%"
    item_prices:List[ItemPriceSchema]

