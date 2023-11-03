from flask import Flask, request, render_template, session, url_for, redirect
import sqlite3

app:Flask = Flask(__name__)
app.secret_key = 'your_secret_key'
app.template_folder = "templates"
app.static_folder = "static"

@app.route('/')
def index():
    return render_template('index.html', header_nike = "")

@app.route('/searchData', methods=['GET', 'POST'])
def searchData(search_text=""):
    sqldbname = 'LapTrinhWeb/python/db/website.db'
    if search_text != "":
        conn=sqlite3.connect(sqldbname)
        cursor = conn.cursor()
        sqlcommand = ("Select * from storages "
                      "where model like '%" +search_text+"%'")
        sqlcommand = sqlcommand + " or brand like '%"+search_text+ "%'"
        sqlcommand = sqlcommand + " or details like '%"+search_text+ "%'"
        
        cursor.execute(sqlcommand)
        data = cursor.fetchall()
        conn.close()
        return data
if __name__ == '__main__':
    app.debug = True
    app.run()
    