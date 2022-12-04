import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database='service_db',
    user='postgres',
    password='2004',
    host='localhost',
    port='5432')
cursor = conn.cursor()
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 0 and (len(username) >= 1 or len(password) >= 1):
                return render_template('No user in db.html'), print(records, password, username)
            elif len(records) == 0:
                return render_template('empty.html'), print(records, password, username)
            else:
                return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if len(name) < 1 and len(login) < 1 and len(password) < 1:
            return render_template('empty2.html')
        if len(login) < 1:
            return render_template('nologin.html')
        if len(password) < 1:
            return render_template('nopass.html')
        if len(name) < 1:
            return render_template('noname.html')
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s,%s,%s);', (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')
