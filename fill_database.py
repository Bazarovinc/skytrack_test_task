#!/usr/bin/env python3
from datetime import datetime
from random import randint, shuffle

from source.database.database import session_local
from source.database.models import Book, Order, OrderItem, Shop, User


def create_test_data():
    session = session_local()

    n = 10
    shops = []
    books = []
    for i in range(n):
        new_user = User(
            first_name=f'first_username_{i}',
            last_name=f'last_username_{i}',
            email=f'email_{i}@mail.ru'
        )
        session.add(new_user)
        new_book = Book(
            name=f'book_name_{i}',
            author=f'book_author_{i}',
            release_date=datetime.utcnow()
        )
        session.add(new_book)
        new_shop = Shop(
            name=f'shop_name_{i}',
            address=f'shop_address_{i}'
        )
        session.add(new_shop)
        session.flush()
        shops.append(new_shop.id)
        books.append(new_book.id)
        number_of_orders = randint(1, n + 1)
        for j in range(number_of_orders):
            new_order = Order(
                reg_date=datetime.utcnow(),
                user_id=new_user.id
            )
            session.add(new_order)
            session.flush()
            shuffle(books)
            shuffle(shops)
            new_order_item = OrderItem(
                book_quantity=randint(1, 10),
                order_id=new_order.id,
                book_id=books[0],
                shop_id=shops[0]
            )
            session.add(new_order_item)
    session.commit()


if __name__ == '__main__':
    create_test_data()
