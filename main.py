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
    sqldbname = 'db/data.db'
    if search_text != "":
        conn=sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = ("Select * from nike "
                      "where model like '%" +search_text+"%'")
        sqlcommand = sqlcommand + " or brand like '%"+search_text+ "%'"
        sqlcommand = sqlcommand + " or details like '%"+search_text+ "%'"
        
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data

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