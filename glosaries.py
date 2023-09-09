from sqlalchemy import  String, Column, Integer , create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///glossaries.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# creation of tables
class User(Base):
    _tablename_ = 'users'

    user_id= Column(Integer, primary_key= True)
    first_name = Column(String(15))
    second_name = Column(String(10))
    surname = Column(String(10))
    email = Column(String(10))
    

class Product (Base):
    _tablename_ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(String)  


class Shopping_Cart(Base):
    _tablename_ = 'bought'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    user_id = Column(String)
    quantity = Column(String)
    pickup_point=Column(String)




Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

