from flask import Flask, render_template, redirect, request, sessions, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'nike'
sqldbname = 'db/nike.db'

@app.route('/')
def index():
    return render_template('register.html',
                           username_error="",
                           email_error="",
                           password_error="",
                           registration_success="")
    
@app.route('/register', methods=['GET', 'POST'])
def SaveToDB(name, email, password):
    id_max = generateID()
    if id_max>0:
        id_max=id_max+1
    else: id_max=1
    print(id_max)
    conn = sqlite3.connect(sqldbname)
    
    cur = conn.cursor()
    cur.execute("INSERT INTO user"
                "(id, name, email, password) VALUES (?, ?, ?, ?)",
                (id_max, name, email, password))
    conn.commit()
    conn.close()
    return id_max

def generateID():
    max_id=0
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT Max(id) from user"
    cursor.execute(sqlcommand)
    max_id=cursor.fetchone()[0]
    return max_id

def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    username_error = ""
    email_error = ""
    password_error = ""
    
    if not username: username_error = "Username is required"
    if not password: password_error = "Password is required"
    if username_error or password_error:
        return render_template('regester.html',
                               username_error=username_error, password_error=password_error,
                               registration_success="")
    newid = SaveToDB(username, email, password)
    stroutput = f'Registered: Username - {username}, Password - {password}'
    registration_success = "Registration Successful! with id = " + str(newid)
    print(registration_success+stroutput)
    return render_template('register.html',
                           password_error="", username_error="",
                           registration_success=registration_success+stroutput)
    
if __name__ == "__main__":
    app.run(debug=True)