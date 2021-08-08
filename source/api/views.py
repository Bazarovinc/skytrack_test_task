from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.router import router
from source.api.schemas.request import NewOrderRequestSchema
from source.api.schemas.response import (CreatedResponseSchema,
                                         OrderResponseSchema)
from source.api.utils import get_order_items_by_order_id
from source.database.database import get_database
from source.database.models import Order, OrderItem, User


@router.get('/user/{user_id}')
async def get_user_info_by_id(user_id: int, db: Session = Depends(get_database)) -> dict:
    if user := db.query(User).filter(User.id == user_id).first():
        return user
    raise HTTPException(status_code=404, detail='User not found')


@router.get('/user_orders_history/{user_id}')
async def get_user_orders_history_by_user_id(user_id: int,  db: Session = Depends(get_database)) -> list:
    if orders_list := db.query(Order).filter(Order.user_id == user_id).all():
        return orders_list
    raise HTTPException(status_code=404, detail=f'No orders for user with id={user_id}')


@router.get('/order/{order_id}')
async def get_order_info_by_id(order_id: int, db: Session = Depends(get_database)) -> OrderResponseSchema:
    if order := db.query(Order).filter(Order.id == order_id).first():
        return OrderResponseSchema(
            id=order.id,
            reg_date=order.reg_date,
            order_items=get_order_items_by_order_id(order_id, db)
        )
    raise HTTPException(status_code=404, detail='Order not found')


@router.post('/new_order', status_code=201)
async def create_new_order(order: NewOrderRequestSchema, db: Session = Depends(get_database)) -> CreatedResponseSchema:
    new_order = Order(
        reg_date=datetime.utcnow(),
        user_id=order.user_id
    )
    db.add(new_order)
    db.flush()
    for order_item in order.order_items:
        new_order_item = OrderItem(
            book_quantity=order_item.book_quantity,
            order_id=new_order.id,
            book_id=order_item.book_id,
            shop_id=order_item.shop_id
        )
        db.add(new_order_item)
    db.commit()
    return CreatedResponseSchema(message='New order was created')
