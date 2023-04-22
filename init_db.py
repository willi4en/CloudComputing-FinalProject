import sqlite3
import csv

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()

cursor = connection.cursor()

# Storing household table
householdFile = open('./data/400_households.csv')
householdContents = csv.reader(householdFile)
next(householdContents)
insert_households = "INSERT INTO households (HSHD_NUM, L, AGE_RANGE, MARITAL, INCOME_RANGE, HOMEOWNER, HSHD_COMPOSITION, HH_SIZE, CHILDREN) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_households, householdContents)

# Storing products table
productsFile = open('./data/400_products.csv')
productsContents = csv.reader(productsFile)
next(productsContents)
insert_products = "INSERT INTO products (PRODUCT_NUM, DEPARTMENT, COMMODITY, BRAND_TY, NATURAL_ORGANIC_FLAG) VALUES(?, ?, ?, ?, ?)"
cursor.executemany(insert_products, productsContents)

# Storing transactions table
transactionsFile = open('./data/400_transactions.csv')
transactionsContents = csv.reader(transactionsFile)
next(transactionsContents)
insert_transactions = "INSERT INTO transactions (BASKET_NUM, HSHD_NUM, PURCHASE, PRODUCT_NUM, SPEND, UNITS, STORE_R, WEEK_NUM, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_transactions, transactionsContents)

connection.commit()

connection.close()
