from flask import Flask, request, render_template, session, url_for, redirect
from flask import Blueprint
import sqlite3

your_product:Flask = Flask(__name__)
your_product.secret_key = 'your_secret_key'
your_product.template_folder = "templates"
your_product.static_folder = "static"
your_product = Blueprint("your_product", __name__)

#tim kiem san pham trong database
@your_product.route("/search", methods=['GET', 'POST'])
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
    
@your_product.route("/searchData", methods=['GET', 'POST'])
def searchData():
    if 'searchInput' in request.form:
        search_text=request.form['searchInput']
        html_table = load_data_from_db(search_text=search_text)
        print(html_table)
        return render_template('search.html',
                            search_text=search_text,
                            table=html_table)
    
@your_product.route("/cart/add", methods=['GET', 'POST']) 
def add_to_cart():  
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
        f'</br>Tiếp tục mua hàng! <a href="/searchData">Trang sản phẩm</a>'
        f'</br>Xem giỏ hàng! <a href="/viewcart">Xem giỏ hàng</a>'
    )
    return outputmessage
    #return render_template('cartadd.html', carts=cart, user_name=cart)