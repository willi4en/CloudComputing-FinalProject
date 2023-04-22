import os
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def hello():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
