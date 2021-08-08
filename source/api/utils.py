from typing import List

from sqlalchemy.orm import Session

from source.api.schemas.base_schemas import BookSchema, OrderItemSchema, ShopSchema
from source.database.models import Book, OrderItem, Shop


def get_order_items_by_order_id(order_id: int, db: Session) -> List[OrderItemSchema]:
    return [OrderItemSchema(
                id=order_item.id,
                order_id=order_id,
                book_quantity=order_item.book_quantity,
                book=BookSchema(
                    id=order_item.book.id,
                    name=order_item.book.name,
                    author=order_item.book.author,
                    release_date=order_item.book.release_date
                ),
                shop=ShopSchema(
                    id=order_item.shop.id,
                    name=order_item.shop.name,
                    address=order_item.shop.address
                )
            )
        for order_item in
            db.query(OrderItem).join(Book, OrderItem.book_id == Book.id).join(Shop, OrderItem.book_id == Shop.id).filter(
            OrderItem.order_id == order_id).all()
    ]
