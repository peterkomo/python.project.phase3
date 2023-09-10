from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
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
    price = Column(Float)

    # Add a foreign key reference to PickupPoint
    pickup_point_id = Column(Integer, ForeignKey('pickup_points.id'))
    pickup_point = relationship("PickupPoint")

    cart_entries = relationship("Shopping_Cart", back_populates="product")

class Shopping_Cart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quantity = Column(Integer)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_entries")

class PickupPoint(Base):
    __tablename__ = 'pickup_points'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address = Column(String(200))
    contact = Column(String(100))

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
    product_price = float(input("Product Price: "))

    new_product = Product(name=product_name, quantity=product_quantity, price=product_price)
    session.add(new_product)
    session.commit()

    print(f"Product {product_name} with quantity {product_quantity} and price ${product_price:.2f} has been created.")

def add_dummy_products():
    store_a = PickupPoint(name="Store A", address="123 Main St", contact="Phone: (123) 456-7890")
    store_b = PickupPoint(name="Store B", address="456 Elm St", contact="Phone: (987) 654-3210")

    dummy_products = [
        {"name": "Apple", "quantity": 100, "price": 1.00, "pickup_point": store_a},
        {"name": "Banana", "quantity": 50, "price": 0.75, "pickup_point": store_b},
        {"name": "Orange", "quantity": 75, "price": 1.25, "pickup_point": store_a},
    ]

    for product_info in dummy_products:
        product = Product(name=product_info["name"], quantity=product_info["quantity"], price=product_info["price"], pickup_point=product_info["pickup_point"])
        session.add(product)

    session.commit()

def add_dummy_pickup_points():
    dummy_pickup_points = [
        {"name": "Store A", "address": "123 Main St", "contact": "Phone: (123) 456-7890"},
        {"name": "Store B", "address": "456 Elm St", "contact": "Phone: (987) 654-3210"},
    ]

    for point_info in dummy_pickup_points:
        pickup_point = PickupPoint(name=point_info["name"], address=point_info["address"], contact=point_info["contact"])
        session.add(pickup_point)

    session.commit()

def view_shopping_cart(user):
    print(f"Shopping Cart for {user.user_first_name} {user.user_surname}:")
    cart_entries = session.query(Shopping_Cart).filter_by(user_id=user.user_id).all()

    if not cart_entries:
        print("Your shopping cart is empty.")
    else:
        total_cost = 0
        for cart_entry in cart_entries:
            product = cart_entry.product
            subtotal = cart_entry.quantity * product.price
            total_cost += subtotal
            print(f"Product: {product.name}, Quantity: {cart_entry.quantity}, Subtotal: ${subtotal:.2f}")

        print(f"Total Cost: ${total_cost:.2f}")

        place_order_option = input("Do you want to place an order? (yes/no): ").strip().lower()
        if place_order_option == "yes":
            place_order(user, total_cost)
        else:
            print("Order not placed. Returning to the main menu.")

def place_order(user, total_cost):
    till_number = "12458"
    print(f"Order placed successfully! Your till number is: {till_number}")
    clear_shopping_cart(user)

def clear_shopping_cart(user):
    session.query(Shopping_Cart).filter_by(user_id=user.user_id).delete()
    session.commit()

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
        print(f"ID: {product.id}, Name: {product.name}, Quantity: {product.quantity}, Price: ${product.price:.2f}, Pick-up Point: {product.pickup_point.name}")

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
    add_dummy_pickup_points()
    add_dummy_products()
    main()
