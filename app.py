import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password='lada',
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(username) == 0 or len(password) == 0:
        return "Вы не ввели логин или пароль!"
    try:
        cursor.execute("SELECT * FROM service.users WHERE login='%s'" %(str(username)))
        records = list(cursor.fetchall())
        if records[0][3] != password:
            return "Неверный пароль"
        return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
    except:
        return "Пользователь не найден"
