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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
