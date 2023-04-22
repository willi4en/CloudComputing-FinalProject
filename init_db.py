import sqlite3
import csv
import pandas

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()

cursor = connection.cursor()

householdFile = open('./data/400_households.csv')
householdContents = csv.reader(householdFile)
insert_households = "INSERT INTO households (HSHD_NUM, L, AGE_RANGE, MARITAL, INCOME_RANGE, HOMEOWNER, HSHD_COMPOSITION, HH_SIZE, CHILDREN) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_households, householdContents)

# df = pandas.read_csv("./data/400_households.csv")
# df.to_sql("households", connection, if_exists='append', index=False)
# df = pandas.read_csv("./data/products.csv")
# df.to_sql("products", connection, if_exists='append', index=False)
# df = pandas.read_csv("./data/transactions.csv")
# df.to_sql("transactions", connection, if_exists='append', index=False)

connection.commit()

connection.close()
