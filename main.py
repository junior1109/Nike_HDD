from flask import Flask, request, render_template, session, url_for, redirect
import sqlite3

app:Flask = Flask(__name__)
app.secret_key = 'your_secret_key'
app.template_folder = "templates"
app.static_folder = "static"

@app.route('/')
def index():
    return render_template('index.html', header_nike = "")

if __name__ == '__main__':
    app.debug = True
    app.run()
    