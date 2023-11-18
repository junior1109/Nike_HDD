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
import sqlite3

app:Flask = Flask(__name__)
app.secret_key = 'your_secret_key'
app.template_folder = "templates"
app.static_folder = "static"

# Hien trang chu len
@app.route('/')
def index():
    return render_template("index.html.jinja2", search_text = "")
    
#tim kiem san pham trong database
@app.route("/search", methods=['GET', 'POST'])
def load_data_from_db(search_text=""):
    sqldbname = 'datanike/datanike.db'
    if search_text != "":
        conn=sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = ("Select * from nike "
                      "where product like '%" +search_text+"%'")
        sqlcommand = sqlcommand + " or brand like '%"+search_text+ "%'"
        sqlcommand = sqlcommand + " or details like '%"+search_text+ "%'"
        
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data
    
@app.route("/searchData", methods=['GET', 'POST'])
def searchData():
    search_text=request.form['searchInput']
    html_table = load_data_from_db(search_text=search_text)
    print(html_table)
    return render_template('search.html',
                           search_text=search_text,
                           table=html_table)
    
@app.route("/cart/add", methods=['GET', 'POST'])  # Thêm phương thức GET vào route
def add_to_cart():  # Sửa tên của hàm thành "add_to_cart"
    # 1. Khai báo Database để lấy giá sản phẩm
    sqldbname = 'datanike/datanike.db'
    # 2. Lấy ID sản phẩm và số lượng từ form
    product_id = request.form["product_id"]
    quantity = int(request.form.get("quantity"))    
    # 3. Lấy tên và giá sản phẩm từ cơ sở dữ liệu
    # hoặc thay đổi cấu trúc của giỏ hàng
    with sqlite3.connect(sqldbname) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT product, price, picture, details "
                    "FROM nike WHERE id = ?",
                    (product_id,))
    # 3.1 Lấy một sản phẩm
        product = cursor.fetchone()   
    # 4. Tạo một từ điển cho sản phẩm
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity,
        "picture": product[2],
        "details": product[3]
    }       
    # 5. Lấy giỏ hàng từ session hoặc tạo danh sách rỗng
    cart = session.get("cart", [])       
    # 6. Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    found = False
    for item in cart:
        if item["id"] == product_id:
            # 6.1 Cập nhật số lượng của sản phẩm đã tồn tại
            item["quantity"] += quantity
            found = True
            break
    if not found: 
        # 6.2 Thêm sản phẩm mới vào giỏ hàng
        cart.append(product_dict)        
    # 7. Lưu giỏ hàng trở lại session
    session["cart"] = cart
    # 8. In ra kết quả
    rows = len(cart)
    outputmessage = (
        f'Đã thêm sản phẩm vào giỏ hàng thành công! '
        f'</br>Hiện có: {rows} sản phẩm'
        f'</br>Tiếp tục mua hàng! <a href="/">Trang tìm kiếm</a>'
        f'</br>Xem giỏ hàng! <a href="/viewcart">Xem giỏ hàng</a>'
    )
    return outputmessage
    #return render_template('cartadd.html', carts=cart, user_name=cart)
@app.route("/viewcart", methods=['GET', 'POST'])
def view_cart():
    current_cart = []
    if 'cart' in session:
        current_cart = session.get("cart", [])  # Get current cart from session
    if 'current_username' in session:
        current_username = session['current_user']['name']
    else:
        current_username = ""
    return render_template('viewcart.html', carts=current_cart, user_name=current_username)

@app.route('/update_cart', methods=['POST'])
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
    return redirect(url_for('view_cart'))
    return render_template('viewcart.html', carts=current_cart, user_name=current_username)

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
    return render_template('login.html.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
