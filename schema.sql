DROP TABLE IF EXISTS households;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

CREATE TABLE households (
    HSHD_NUM INTEGER PRIMARY KEY,
    L TEXT,
    AGE_RANGE TEXT,
    MARITAL TEXT,
    INCOME_RANGE TEXT,
    HOMEOWNER TEXT,
    HSHD_COMPOSITION TEXT,
    HH_SIZE TEXT,
    CHILDREN TEXT
);                                                                                                                                                                                               
         
CREATE TABLE products (
    PRODUCT_NUM INTEGER PRIMARY KEY,
    DEPARTMENT TEXT,
    COMMODITY TEXT,
    BRAND_TY TEXT,
    NATURAL_ORGANIC_FLAG TEXT
);

CREATE TABLE transactions (
    TRANSACTION_NUM INTEGER PRIMARY KEY,
    BASKET_NUM INTEGER NOT NULL,
    HSHD_NUM INTEGER NOT NULL,
    PURCHASE TIMESTAMP,
    PRODUCT_NUM INTEGER,
    SPEND FLOAT,
    UNITS INTEGER,
    STORE_R TEXT,
    WEEK_NUM INTEGER,
    YEAR INTEGER
);

CREATE TABLE users (
    USER_KEY INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);