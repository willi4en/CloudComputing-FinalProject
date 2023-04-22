import os
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    try:
        connection = sqlite3.connect('database.db')
    except Exception as e:
        print("Oof", e)
        if connection:
            connection.close()
    return connection


def get_data(hshd_num=10):
    data = []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM households WHERE HSHD_NUM = (?)", [10])
    household_data = cur.fetchone()
    cur.execute("SELECT * FROM transactions WHERE HSHD_NUM = (?)", [10])
    transactions_data = cur.fetchall()
    for transaction in transactions_data:
        product_num = transaction[4]
        cur.execute("SELECT * FROM products WHERE PRODUCT_NUM = (?)", [product_num])
        product_data = cur.fetchall()
        for product in product_data:
            table_row = {
            'HSHD_NUM': 10,
            'AGE_RANGE': household_data[2],
            'BASKET_NUM': transaction[1],
            'PURCHASE': transaction[3],
            'PRODUCT_NUM': transaction[4],
            'DEPARTMENT': product[1],
            'COMMODITY': product[2],
            'SPEND': transaction[5],
            'UNITS': transaction[6],
            'STORE_R': transaction[7],
            'WEEK_NUM': transaction[8],
            'LOYALTY_FLAG': household_data[1],
            'YEAR': transaction[9],
            'MARITAL': household_data[3],
            'HOMEOWNER': household_data[5],
            'INCOME_RANGE': household_data[4],
            'HSHD_COMPOSITION': household_data[6],
            'HH_SIZE' : household_data[7],
            'CHILDREN': household_data[8]
            }
            data.append(table_row)
    return data


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            return render_template('login.html', error="Please make sure all fields are filled out.")
        cur.execute(
            "SELECT * from users where username = (?) AND password = (?)", [username, password])
        user = cur.fetchone()
        if (user is not None):
            conn.close()
            session['currentUser'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            conn.close()
            return render_template('login.html', error="Invalid Login: Please try again.")
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/account_creation', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, email) VALUES (?,?,?)", [
                    username, password, email])
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('createAccount.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        return redirect(url_for('home'))
    else:
        currentUser = session['currentUser']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE USER_KEY = (?)", [currentUser])
        user = cur.fetchone()
        conn.close()
        if (user is None):
            return redirect(url_for('home'))
        else:
            return render_template('dashboard.html')

@app.route('/sample_data_pull_10')
def sample_data_pull_10():
    data = get_data(10)
    return render_template('sample_data_pull_10.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
