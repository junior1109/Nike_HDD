from flask import Flask, request, render_template, session, url_for, redirect
from flask import Blueprint
import sqlite3

your_cart:Flask = Flask(__name__)
your_cart.secret_key = 'your_secret_key'
your_cart.template_folder = "templates"
your_cart.static_folder = "static"
your_cart = Blueprint("your_cart", __name__)

@your_cart.route("/viewcart", methods=['GET', 'POST'])
def view_cart():
    current_cart = []
    if 'cart' in session:
        current_cart = session.get("cart", [])  # Get current cart from session
    if 'current_username' in session:
        current_username = session['current_user']['name']
    else:
        current_username = ""
    return render_template('viewcart.html', carts=current_cart, user_name=current_username)

@your_cart.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', [])
    new_cart=[]
    for product in cart:
        product_id=str(product['id'])
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            # if the quantity is 0 or this is a delete field, skip this product
            if quantity == 0 or f'delete-{product_id}' in request.form: #delete
            #     continue
            #if quantity == 0 or request.form.get(f'delete-{product_id}') == "true":
                continue
            product['quantity']=quantity
        new_cart.append(product)
    session['cart']=new_cart
    return redirect(url_for('your_cart.view_cart'))
    # return render_template('viewcart.html', carts=current_cart, user_name=current_username)

@your_cart.route("/proceed_cart", methods=['GET', 'POST'])
def proceed_cart():
    if 'current_user' in session:
        user_id = session['current_user']['id']
        user_email = session['current_user']['email']
    else:
        user_id = 0
        user_email = 0
    #2. get the shopping cart from the session
    current_cart = []
    if 'cart' in session:
        shopping_cart = session.get("cart", [])
    # 3. save Order Information to the "Order" table
    # Establish a database connection
    sqldbname = 'datanike/datanike.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    # Define the order information (Create a new form)
    user_address = "User Address"
    user_mobile = "User Mobile"
    purchase_date = "2023-10-23"
    ship_date = "2023-10-25"
    status = 1 
    # Insert the order into the "order" table
    cursor.execute('''INSERT INTO "order" (user_id, user_email, 
                   user_address, user_mobile, purchase_date, 
                   ship_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (user_id, user_email, user_address, user_mobile, purchase_date, ship_date, status))
    
    # 4. Get the ID of the inserted order
    order_id = cursor.lastrowid
    print(order_id)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    # 5. save order details to the "order details" table
    # establish a new database connection (or reuse the existing connection)
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    # insert order details into the "order_details" table
    for product in shopping_cart:
        product_id = product['id']
        price = product['price']
        quantity = product['quantity']
        cursor.execute('''INSERT INTO order_details 
                       (order_id, product_id, price, quantity) VALUES (?, ?, ?, ?) ''', (order_id, product_id, price, quantity))
        
    # 6. commit the changes ans close the connection
    conn.commit()
    conn.close()
    # 7. to remove the current_cart from the session
    if 'cart' in session:
        current_cart = session.pop("cart", [])
    else:
        print("No current_cart in session")
    # call to orders/order_id
    order_url = url_for('orders', user_id=user_id, _external=True)
    return f'Redirecting to order page: <a href ="{order_url}">{order_url}</a>'
