import os
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import pandas as pd
import sys

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
    cur.execute("SELECT * FROM households WHERE HSHD_NUM = (?)", [hshd_num])
    household_data = cur.fetchone()
    cur.execute("SELECT * FROM transactions WHERE HSHD_NUM = (?)", [hshd_num])
    transactions_data = cur.fetchall()
    for transaction in transactions_data:
        product_num = transaction[4]
        cur.execute(
            "SELECT * FROM products WHERE PRODUCT_NUM = (?)", [product_num])
        product_data = cur.fetchall()
        for product in product_data:
            table_row = {
                'HSHD_NUM': hshd_num,
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
                'HH_SIZE': household_data[7],
                'CHILDREN': household_data[8]
            }
            data.append(table_row)
    data = pd.DataFrame(data)
    if not data.empty:
        data = data.sort_values(
            ['HSHD_NUM', 'BASKET_NUM', 'PURCHASE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
    else:
        data = pd.DataFrame()
    return data


def get_hshd_attrs(hshd_list):
    data = []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM households WHERE HSHD_NUM IN ({})".format(
        ', '.join(['?']*len(hshd_list))), hshd_list)
    household_data = cur.fetchall()
    for household in household_data:
        table_row = {
            'HSHD_NUM': household[0],
            'LOYALTY_FLAG': household[1],
            'AGE_RANGE': household[2],
            'MARITAL': household[3],
            'INCOME_RANGE': household[4],
            'HOMEOWNER': household[5],
            'HSHD_COMPOSITION': household[6],
            'HH_SIZE': household[7],
            'CHILDREN': household[8]
        }
        data.append(table_row)
    data = pd.DataFrame(data)
    if not data.empty:
        unique_counts = data.nunique().sort_values().head(3)
        # get the most common values in each of the top 3 columns
        most_common = {}
        print(unique_counts.index)
        for col in unique_counts.index:
            most_common[col] = data[col].value_counts().idxmax()
        data = pd.DataFrame([most_common])
    else:
        data = pd.DataFrame()
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


@app.route('/interactive_search', methods=['GET', 'POST'])
def interactive_search():
    if request.method == 'POST':
        hshd_num = request.form['hshd_num']
        data = get_data(hshd_num)
        if data.empty:
            return render_template('interactive_search.html', data=data, hshd_num=hshd_num, error="Selected HSHD # does not exist in the database.")
        else:
            return render_template('interactive_search.html', data=data, hshd_num=hshd_num)
    return render_template('interactive_search.html', data=pd.DataFrame(), hshd_num=None)


@app.route('/demographics')
def demographics():
    conn = get_db_connection()
    cur = conn.cursor()
    # cur.execute(
    #     "SELECT HSHD_NUM FROM transactions GROUP BY HSHD_NUM HAVING COUNT(*) = (SELECT MAX(Cnt) FROM (SELECT COUNT(*) as Cnt FROM transactions GROUP BY HSHD_NUM) tmp)")
    cur.execute(
        "SELECT HSHD_NUM FROM transactions GROUP BY HSHD_NUM ORDER BY COUNT(HSHD_NUM) DESC")
    households = cur.fetchmany(3)
    conn.close()
    houseNums = [households[0][0], households[1][0], households[2][0]]
    houseDF = get_hshd_attrs(houseNums)

    top1Name = houseDF.columns[0]  # households[0][0]
    top2Name = houseDF.columns[1]  # households[1][0]
    top3Name = houseDF.columns[2]  # households[2][0]
    top1Value = houseDF.iat[0, 0]
    top2Value = houseDF.iat[0, 1]
    top3Value = houseDF.iat[0, 2]
    return render_template('demographics.html', top1Name=top1Name, top1Value=top1Value, top2Name=top2Name, top2Value=top2Value, top3Name=top3Name, top3Value=top3Value)


@app.route('/importdata')
def importData():
    return render_template('importData.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
