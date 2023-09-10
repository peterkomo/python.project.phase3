from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_first_name = Column(String(50))
    user_second_name = Column(String(50))
    user_surname = Column(String(50))
    user_email = Column(String(100), unique=True)
    role = Column(String(20), default='customer')
    unique_code = Column(String(10))

    # Establish a one-to-many relationship with Shopping_Cart
    cart_items = relationship('Shopping_Cart', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)

    cart_entries = relationship("Shopping_Cart", back_populates="product")

class Shopping_Cart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quantity = Column(Integer)
    

    # Establish relationships with User and Product
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="cart_items")

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="cart_entries")

    pickup_location_id = Column(Integer, ForeignKey('pickup_locations.id'))
    pickup_location = relationship("PickupLocation", back_populates="cart_entries")


class PickupLocation(Base):
    __tablename__ = 'pickup_locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(100))

    # Relationship to Shopping_Cart
    cart_entries = relationship("Shopping_Cart", back_populates="pickup_location")

    # Other columns and methods...





engine = create_engine('sqlite:///glossaries.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
