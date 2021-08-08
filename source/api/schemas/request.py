from typing import List

from pydantic import BaseModel


class OrderItemRequestSchema(BaseModel):
    book_id: int
    shop_id: int
    book_quantity: int


class NewOrderRequestSchema(BaseModel):
    user_id: int
    order_items: List[OrderItemRequestSchema]
