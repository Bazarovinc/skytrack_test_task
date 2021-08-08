from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    reg_date: datetime


class OrdersHistoryResponseSchema(BaseModel):
    orders: List[OrderResponseSchema]
