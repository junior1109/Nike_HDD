# <!-- Đây là trang chính
#     Viết code nhớ comment
#     Anh em thêm/sửa/xóa code thì nhớ comment lại 
#     Và push code lên git
# -->
# <!-- 
#     git add .
#     git commit -m "comment"
#     git push origin master
#  -->

from flask import Flask, request, render_template, session, url_for, redirect
from main_product import your_product
from main_cart import your_cart
import sqlite3

app:Flask = Flask(__name__)
app.secret_key = 'your_secret_key'
app.template_folder = "templates"
app.static_folder = "static"
app.register_blueprint(your_product)
app.register_blueprint(your_cart)

# Hien trang chu len
@app.route('/')
def index():
    return render_template("index.html", search_text = "")
    
#trang login
@app.route('/login', methods=['GET', 'POST'])
def check_exists(username, password):
    result = False;
    sqldbname = 'db/data.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "Select * from user where name = '"+username+"' and password = '"+password+"'"
    cursor.execute(sqlcommand)
    data = cursor.fetchall()
    print(type(data))
    if len(data)>0:
        result = True
    conn.close()
    return result;
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_exists(username, password):
            session['username'] = username 
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/orders/', defaults={'order_id': None}, methods=['GET'])
@app.route('/orders/<int:order_id>/', methods=['GET'])
def orders(order_id):
    sqldbname = 'datanike/datanike.db'
    user_id = session.get('current_user', {}.get('if'))
    if user_id:
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        if order_id is not None:
            cursor.execute('SELECT * FROM "order" WHERE id = ? AND user_id = ?'(order_id=order_id))
            order = cursor.fetchone()
            cursor.execute('SELECT * FROM order_details WHERE order_id = ?', (order_id,))
            order_details = cursor.fetchall()
            conn.close()
            return render_template('order_details.html', order=order, order_details=order_details)
        else:
            cursor.execute('SELECT * FROM "order" WHERE user_id = ?', (user_id,))
            user_orders = cursor.fetchall()
            conn.close()
            return render_template('orders.html', orders=user_orders)
    return "Use not logged in"



if __name__ == '__main__':
    app.run(debug=True)
