import datetime

from fastapi.testclient import TestClient
from source.database.database import session_local
from source.database.models import Book, Order, OrderItem, Shop, User
from tests.schemas import OrdersHistoryResponseSchema
from source.api.utils import get_order_items_by_order_id
from source.api.schemas.response import OrderResponseSchema
from source.api.schemas.request import NewOrderRequestSchema, OrderItemRequestSchema

from main import app

client = TestClient(app)
session = session_local()


def test_root_view():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world!'}


def test_get_user_info_by_id_view():
    """Case #1: user found in database, status 200, returned user info"""
    if user := session.query(User).filter(User.id == 1).first():
        response = client.get('/api/user/1')
        assert response.status_code == 200
        assert response.json() == {
                'id': user.id,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name
            }
    """Case #2: user not found, 404"""
    response = client.get('/api/user/1000000000000000')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_get_user_orders_history_by_user_id_view():
    """Case #1: found orders for user with such id, status 200"""
    if orders_list := session.query(Order).filter(Order.user_id == 1).all():
        response = client.get('/api/user_orders_history/1')
        assert response.status_code == 200
        response_orders_list = OrdersHistoryResponseSchema(orders=response.json())
        for i, order in enumerate(orders_list):
            assert response_orders_list.orders[i].id == order.id
            assert response_orders_list.orders[i].user_id == order.user_id
            assert response_orders_list.orders[i].reg_date == order.reg_date
    """Case #2: no orders for user with id, 404"""
    response = client.get('/api/user_orders_history/1000000000000')
    assert response.status_code == 404
    assert response.json() == {'detail': 'No orders for user with id=1000000000000'}


def test_get_order_info_by_id_view():
    """Case #1: order found, status 200"""
    if order := session.query(Order).filter(Order.id == 1).first():
        order_schema = OrderResponseSchema(
            id=order.id,
            reg_date=order.reg_date,
            order_items=get_order_items_by_order_id(order.id, session)
        )
        response = client.get('/api/order/1')
        assert response.status_code == 200
        assert OrderResponseSchema(**response.json()) == order_schema
    """Case #2: order not found, 404"""
    response = client.get('/api/order/1000000000000')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Order not found'}


def test_create_new_order_view():
    new_order = NewOrderRequestSchema(
        user_id=1,
        order_items=[OrderItemRequestSchema(**{'book_id': 1, 'shop_id': 1, 'book_quantity': 1})]
    )
    response = client.post('api/new_order', data=new_order.json())
    assert response.status_code == 201
    assert response.json() == {'message': 'New order was created'}
    added_order = session.query(Order).filter(Order.user_id == 1).all()
    added_order = added_order[-1]
    assert added_order.user_id == new_order.user_id
    assert added_order.reg_date <= datetime.datetime.utcnow()
    added_order_item = session.query(OrderItem).filter(OrderItem.order_id == added_order.id).first()
    assert added_order_item.book_id == new_order.order_items[0].book_id
    assert added_order_item.shop_id == new_order.order_items[0].shop_id
    assert added_order_item.book_quantity == new_order.order_items[0].book_quantity



