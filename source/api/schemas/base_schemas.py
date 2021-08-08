from datetime import date

from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    name: str
    author: str
    release_date: date


class ShopSchema(BaseModel):
    id: int
    name: str
    address: str


class OrderItemSchema(BaseModel):
    id: int
    order_id: int
    book: BookSchema
    shop: ShopSchema
    book_quantity: int
