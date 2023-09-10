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
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_entries")

engine = create_engine('sqlite:///trial.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_new_user():
    print("Please add your details:")
    usr_fn = input("First Name: ")
    usr_sn = input("Second Name: ")
    usr_uc = input("Surname: ")
    usr_em = input("Email: ")

    new_user = User(user_first_name=usr_fn, user_second_name=usr_sn, user_surname=usr_uc, user_email=usr_em)
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(user_email=usr_em).first()
    new_user_code = f"s{usr_fn[0]}{usr_sn[0]}{user.user_id}{usr_uc[-1]}"
    user.unique_code = new_user_code
    session.commit()

    print(f"Thank you for registering with us. Your login code is {new_user_code}")

def create_product():
    print("Please add product details:")
    product_name = input("Product Name: ")
    product_quantity = int(input("Product Quantity: "))

    new_product = Product(name=product_name, quantity=product_quantity)
    session.add(new_product)
    session.commit()

    print(f"Product {product_name} with quantity {product_quantity} has been created.")

def view_shopping_cart(user):
    print("\nYour Shopping Cart:")
    cart_entries = session.query(Shopping_Cart).filter_by(user_id=user.user_id).all()

    if not cart_entries:
        print("Your shopping cart is empty.")
        return

    total_cost = 0

    for entry in cart_entries:
        product = session.query(Product).filter_by(id=entry.product_id).first()
        if product:
            cost = product.quantity * entry.quantity
            print(f"Product: {product.name}, Quantity: {entry.quantity}, Cost: {cost}")
            total_cost += cost
        else:
            print(f"Product for this entry not found in the product list. Please remove it from your cart.")

    print(f"Total Cost: {total_cost}")

def main():
    print("Welcome to Uncle Pete's groceries system")
    print("Are you an existing member?")
    print("1. Yes")
    print("2. No")

    get_choice = input("Choose one: ")

    if get_choice == "1":
        usr_em = input("Please enter your email: ")
        user = session.query(User).filter_by(user_email=usr_em).first()
        if user:
            print(f"Welcome back, {user.user_first_name}!")
            shopping_menu(user)
        else:
            print("User not found.")
    elif get_choice == "2":
        create_new_user()
    else:
        print("Invalid choice. Please choose 1 or 2.")

def shopping_menu(user):
    while True:
        print("\nShopping Menu:")
        print("1. Browse Products")
        print("2. View Shopping Cart")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            browse_products(user)
        elif choice == "2":
            view_shopping_cart(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

def browse_products(user):
    print("\nAvailable Products:")
    products = session.query(Product).all()

    if not products:
        print("No products available.")
        return

    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Quantity: {product.quantity}")

    while True:
        product_id = input("Enter the ID of the product you want to add to your cart (0 to exit): ")

        if product_id == "0":
            return
        elif not product_id.isdigit():
            print("Invalid input. Please enter a valid product ID.")
            continue

        product_id = int(product_id)

        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            while True:
                quantity = input("Enter the quantity: ")

                if not quantity.isdigit():
                    print("Invalid input. Please enter a valid quantity.")
                    continue

                quantity = int(quantity)

                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                elif quantity > product.quantity:
                    print("Insufficient quantity available.")
                else:
                    add_to_shopping_cart(user, product, quantity)
                    print(f"{quantity} {product.name} added to your shopping cart.")
                    break
        else:
            print("Product not found. Please enter a valid product ID.")

def add_to_shopping_cart(user, product, quantity):
    cart_entry = session.query(Shopping_Cart).filter_by(user_id=user.user_id, product_id=product.id).first()

    if cart_entry:
        cart_entry.quantity += quantity
    else:
        new_cart_entry = Shopping_Cart(user=user, product=product, quantity=quantity)
        session.add(new_cart_entry)

    session.commit()

if __name__ == "__main__":
    main()
