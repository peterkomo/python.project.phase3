from glosaries import User, Product , Shopping_Cart
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

from tabulate import tabulate

def creating_new_user():

    # Promts users to enter required information
    print("Please add your details:")
    usr_id = None
    usr_fn = input("First Name: ")
    usr_Sn = input("Second name: ")  
    usr_uc = input("Surname:  ")
    usr_em = input("email")
    

    # Adds new student to the database
    new_user = User( user_id=usr_id,user_first_name = usr_fn, user_second_name = usr_Sn, user_surname = usr_uc, user_email = usr_em)
    session.add(new_user)
    session.commit()

    # Finds new student to assign them a new unique key
    user_code = session.query(User).all()
    for user in user_code:
            if user.user_first_name == usr_fn and user.user_second_name == usr_Sn and user.user_surname == usr_uc :
        
            # add the student unique code.
            
                add_unique_code = session.query(User).filter(User.student_id == user.student_id).first()                    
            # Gives criteria of assigning the new student indentification code

            new_user_code =f"s{user.user_first_name[0]}{user.user_first_name[2]}{user.student_id}{user.user_surname[-1]}"
            add_unique_code.unique_code = new_user_code
            session.commit()

            # message to confirm registration
            print(f"Thank you for registering with us you log in code is {new_student_code}")

def read_user(user_id):
    # Read user information by user_id
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        print(f"User ID: {user.user_id}")
        print(f"First Name: {user.first_name}")
        print(f"Second Name: {user.second_name}")
        print(f"Surname: {user.surname}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
    else:
        print(f"User with ID {user_id} not found.")

def update_user(user_id):
    # Update user information by user_id
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        print(f"Update user information (leave blank to keep current values):")
        usr_fn = input(f"First Name ({user.first_name}): ") or user.first_name
        usr_sn = input(f"Second Name ({user.second_name}): ") or user.second_name
        usr_uc = input(f"Surname ({user.surname}): ") or user.surname
        usr_em = input(f"Email ({user.email}): ") or user.email

        user.first_name = usr_fn
        user.second_name = usr_sn
        user.surname = usr_uc
        user.email = usr_em

        session.commit()
        print(f"User {user_id} has been updated.")
    else:
        print(f"User with ID {user_id} not found.")

def delete_user(user_id):
    # Delete user by user_id
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User {user_id} has been deleted.")
    else:
        print(f"User with ID {user_id} not found.")

def create_product():
    # Prompt users to enter product details
    print("Please add product details:")
    product_name = input("Product Name: ")
    product_quantity = int(input("Product Quantity: "))

    # Create and add a new product to the database
    new_product = Product(name=product_name, quantity=product_quantity)
    session.add(new_product)
    session.commit()

    print(f"Product {product_name} with quantity {product_quantity} has been created.")

def read_product(product_id):
    # Read product information by product_id
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        print(f"Product ID: {product.id}")
        print(f"Product Name: {product.name}")
        print(f"Product Quantity: {product.quantity}")
    else:
        print(f"Product with ID {product_id} not found.")

def update_product(product_id):
    # Update product information by product_id
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        print(f"Update product information (leave blank to keep current values):")
        product_name = input(f"Product Name ({product.name}): ") or product.name
        product_quantity = int(input(f"Product Quantity ({product.quantity}): ")) or product.quantity

        product.name = product_name
        product.quantity = product_quantity

        session.commit()
        print(f"Product {product_id} has been updated.")
    else:
        print(f"Product with ID {product_id} not found.")

def delete_product(product_id):
    # Delete product by product_id
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        session.delete(product)
        session.commit()
        print(f"Product {product_id} has been deleted.")
    else:
        print(f"Product with ID {product_id} not found.")
def create_shopping_cart():
    # Prompt users to enter shopping cart details
    print("Please add shopping cart details:")
    product_name = input("Product Name: ")
    user_id = int(input("User ID: "))
    quantity = int(input("Quantity: "))
    pickup_point = input("Pickup Point: ")

    # Create and add a new shopping cart entry to the database
    new_cart_entry = Shopping_Cart(product_name=product_name, user_id=user_id, quantity=quantity, pickup_point=pickup_point)
    session.add(new_cart_entry)
    session.commit()

    print(f"Shopping cart entry for Product {product_name}, User ID {user_id} with quantity {quantity} has been created.")

def read_shopping_cart(cart_id):
    # Read shopping cart entry information by cart_id
    cart_entry = session.query(Shopping_Cart).filter_by(id=cart_id).first()
    if cart_entry:
        print(f"Cart Entry ID: {cart_entry.id}")
        print(f"Product Name: {cart_entry.product_name}")
        print(f"User ID: {cart_entry.user_id}")
        print(f"Quantity: {cart_entry.quantity}")
        print(f"Pickup Point: {cart_entry.pickup_point}")
    else:
        print(f"Shopping cart entry with ID {cart_id} not found.")

def update_shopping_cart(cart_id):
    # Update shopping cart entry information by cart_id
    cart_entry = session.query(Shopping_Cart).filter_by(id=cart_id).first()
    if cart_entry:
        print(f"Update shopping cart entry information (leave blank to keep current values):")
        product_name = input(f"Product Name ({cart_entry.product_name}): ") or cart_entry.product_name
        user_id = int(input(f"User ID ({cart_entry.user_id}): ")) or cart_entry.user_id
        quantity = int(input(f"Quantity ({cart_entry.quantity}): ")) or cart_entry.quantity
        pickup_point = input(f"Pickup Point ({cart_entry.pickup_point}): ") or cart_entry.pickup_point

        cart_entry.product_name = product_name
        cart_entry.user_id = user_id
        cart_entry.quantity = quantity
        cart_entry.pickup_point = pickup_point

        session.commit()
        print(f"Shopping cart entry {cart_id} has been updated.")
    else:
        print(f"Shopping cart entry with ID {cart_id} not found.")

def delete_shopping_cart(cart_id):
    # Delete shopping cart entry by cart_id
    cart_entry = session.query(Shopping_Cart).filter_by(id=cart_id).first()
    if cart_entry:
        session.delete(cart_entry)
        session.commit()
        print(f"Shopping cart entry {cart_id} has been deleted.")
    else:
        print(f"Shopping cart entry with ID {cart_id} not found.")
def main():
    print("Welcome to Uncle Pete's groceries system")
    print("Are you an existing member?")
    print("1. Yes")
    print("2. No")

    get_choice = input("Choose one: ")

    if get_choice == "1":
        user_id = input("Please enter your user number: ")
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            print(f"Welcome back, {user.first_name}!")
            shopping_menu(user)
        else:
            print("User not found.")
    elif get_choice == "2":
        creating_new_user()
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
    products = [
        {"id": 1, "name": "apple", "quantity": 10},
        {"id": 2, "name": "Pinaple", "quantity": 5},
        {"id": 3, "name": "sukuma wiki", "quantity": 10},
        {"id": 4, "name": "spinach", "quantity": 10},
        {"id": 5, "name": "passion", "quantity": 10},
        {"id": 6, "name": "kiwi", "quantity": 10},
        {"id": 7, "name": "managu", "quantity": 10},
        {"id": 8, "name": "cabbage", "quantity": 10},
        {"id": 9, "name": "waru", "quantity": 10},
        {"id": 10, "name": "minji", "quantity": 10},
        {"id": 11, "name": "hoho", "quantity": 10},
        # Add more product details as needed
    ]

    for product in products:
        print(f"ID: {product['id']}, Name: {product['name']}, Quantity: {product['quantity']}")

    product_id = input("Enter the ID of the product you want to add to your cart (0 to exit): ")

    if product_id == "0":
        return
    else:
        product = next((p for p in products if p["id"] == int(product_id)), None)
        if product:
            quantity = int(input("Enter the quantity: "))
            if quantity <= product["quantity"]:
                add_to_shopping_cart(user, product, quantity)
            else:
                print("Insufficient quantity available.")
        else:
            print("Product not found.")
def add_to_shopping_cart(user, product, quantity):
    new_cart_entry = Shopping_Cart(product_name=product.name, user_id=user.user_id, quantity=quantity, pickup_point=user.email)
    session.add(new_cart_entry)
    session.commit()
    print(f"{quantity} {product.name} added to your shopping cart.")

def view_shopping_cart(user):
    print("\nYour Shopping Cart:")
    cart_entries = session.query(Shopping_Cart).filter_by(user_id=user.user_id).all()

    if not cart_entries:
        print("Your shopping cart is empty.")
        return

    total_cost = 0

    for entry in cart_entries:
        product = session.query(Product).filter_by(name=entry.product_name).first()
        cost = product.quantity * entry.quantity
        print(f"Product: {entry.product_name}, Quantity: {entry.quantity}, Cost: {cost}")
        total_cost += cost

    print(f"Total Cost: {total_cost}")

if __name__ == "__main__":
    main()            ; 

