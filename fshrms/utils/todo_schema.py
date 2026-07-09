from typing import List

from pydantic import BaseModel, Field


class ItemPriceSchema(BaseModel):
    price_list: str = "Standard Selling"
    price_list_rate: float


class ItemCreateSchema(BaseModel):
    item_code: str
    item_name: str
    item_group: str = "Products"
    stock_uom: str = "Nos"
    is_stock_item: int = 1
    standard_rate: float = 0
    item_tax_template: str | None = None
    item_prices: List[ItemPriceSchema] = Field(
        default_factory=list
    )


class ItemUpdateSchema(BaseModel):
    item_name: str | None = None
    item_group: str | None = None
    stock_uom: str | None = None
    is_stock_item: int | None = None

    standard_rate: float | None = None

    item_tax_template: str | None = None

    item_prices: List[ItemPriceSchema] = Field(
        default_factory=list
    )