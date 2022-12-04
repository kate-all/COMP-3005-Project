DROP DATABASE IF EXISTS "LookInnaBook";
CREATE DATABASE "LookInnaBook";

CREATE TABLE PUBLISHER (
   publisher_id CHAR(10) NOT NULL PRIMARY KEY,
   name VARCHAR(20) NOT NULL,
   email VARCHAR(30) UNIQUE NOT NULL,
   phone_number NUMERIC(10,0) UNIQUE,
   bank_acc_num NUMERIC(17,0) NOT NULL
);

CREATE TABLE BOOK (
    isbn NUMERIC(13,0) NOT NULL PRIMARY KEY,
    title VARCHAR NOT NULL,
    page_count INT,
    price NUMERIC(4,2) NOT NULL,
    num_sold INT,
    num_sold_last_month INT,
    percent_for_publisher NUMERIC(3,2) NOT NULL,
    wholesale_price NUMERIC(4,2) NOT NULL,
    publisher_id CHAR(10) NOT NULL,
    FOREIGN KEY (publisher_id)
                  REFERENCES Publisher(publisher_id)
);

CREATE TABLE ADDRESS (
    street_num INT NOT NULL,
    street VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    province CHAR(2) NOT NULL,
    country VARCHAR(30) NOT NULL,
    postal_code CHAR(6) NOT NULL,
    PRIMARY KEY (street_num, street, postal_code)
);

CREATE TABLE ORDERS (
    order_num NUMERIC(5,0) NOT NULL PRIMARY KEY,
    postal_code CHAR(6) NOT NULL,
    street VARCHAR(20) NOT NULL,
    street_num INT NOT NULL,
    current_city VARCHAR(20) NOT NULL,
    eta DATE,
    FOREIGN KEY (postal_code, street, street_num)
                REFERENCES Address(postal_code, street, street_num)
);

CREATE TABLE AUTHOR (
    author_id CHAR(10) NOT NULL PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20) NOT NULL
);

CREATE TABLE CREDIT_CARD (
    card_num NUMERIC(16,0) NOT NULL PRIMARY KEY,
    expiry_date DATE NOT NULL,
    cvv NUMERIC(3,0) NOT NULL
);

CREATE TABLE ACCOUNT (
    username VARCHAR(20) NOT NULL PRIMARY KEY,
    password VARCHAR(20) NOT NULL
);

CREATE TABLE GENRE (
    name VARCHAR(20) NOT NULL PRIMARY KEY
);

CREATE TABLE WRITTEN_BY (
    book_isbn NUMERIC(13,0) NOT NULL,
    author_id CHAR(10) NOT NULL,
    PRIMARY KEY (book_isbn, author_id),
    FOREIGN KEY (book_isbn)
                REFERENCES Book(isbn),
    FOREIGN KEY (author_id)
                REFERENCES Author(author_id)
);

CREATE TABLE HAS_GENRE (
    book_isbn NUMERIC(13,0) NOT NULL,
    genre VARCHAR(20) NOT NULL,
    PRIMARY KEY (book_isbn, genre),
    FOREIGN KEY (genre)
                REFERENCES Genre(name),
    FOREIGN KEY (book_isbn)
                REFERENCES Book(isbn)
);

CREATE TABLE INCLUDES (
    order_num NUMERIC(5,0) NOT NULL,
    book_isbn NUMERIC(13,0) NOT NULL,
    PRIMARY KEY (order_num, book_isbn),
    FOREIGN KEY (order_num)
                REFERENCES Orders(order_num),
    FOREIGN KEY (book_isbn)
                REFERENCES Book(isbn)
);

CREATE TABLE PAID_WITH (
    card_num NUMERIC(16,0) NOT NULL,
    order_num NUMERIC(5,0) NOT NULL,
    PRIMARY KEY (card_num, order_num),
    FOREIGN KEY (card_num)
                REFERENCES Credit_Card(card_num),
    FOREIGN KEY (order_num)
                REFERENCES Orders(order_num)
);

CREATE TABLE CHARGES_TO (
    account_name VARCHAR(20) NOT NULL,
    credit_card NUMERIC(16,0) NOT NULL,
    PRIMARY KEY (account_name, credit_card),
    FOREIGN KEY (account_name)
                REFERENCES Account(username),
    FOREIGN KEY (credit_card)
                REFERENCES Credit_Card(card_num)
);

CREATE TABLE SHIPS_TO (
    account_name VARCHAR(20) NOT NULL,
    postal_code CHAR(6) NOT NULL,
    street VARCHAR(20) NOT NULL,
    street_num INT NOT NULL,
    PRIMARY KEY (account_name, postal_code, street, street_num),
    FOREIGN KEY (account_name)
                REFERENCES Account(username),
    FOREIGN KEY (postal_code, street, street_num)
                REFERENCES Address(postal_code, street, street_num)
);