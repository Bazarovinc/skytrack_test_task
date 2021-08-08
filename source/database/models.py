from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from .database import Base


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    orders = relationship('Order')


class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)


class Shop(Base):
    __tablename__ = 'Shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    reg_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    order_items = relationship("OrderItem")


class OrderItem(Base):
    __tablename__ = 'OrderItem'

    id = Column(Integer, primary_key=True)
    book_quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('Order.id'))
    book_id = Column(Integer, ForeignKey('Book.id'))
    shop_id = Column(Integer, ForeignKey('Shop.id'))
    book = relationship("Book")
    shop = relationship("Shop")
