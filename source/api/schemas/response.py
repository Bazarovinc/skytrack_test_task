from datetime import datetime
from typing import List

from pydantic import BaseModel
from source.api.schemas.base_schemas import OrderItemSchema


class OrderResponseSchema(BaseModel):
    id: int
    reg_date: datetime
    order_items: List[OrderItemSchema]


class UserOrdersHistoryResponseSchema(BaseModel):
    orders: List[OrderResponseSchema]


class CreatedResponseSchema(BaseModel):
    message: str
