DROP DATABASE IF EXISTS 'LookInnaBook';
CREATE DATABASE 'LookInnaBook';

CREATE TABLE PUBLISHER (
   publisher_id CHAR(10) NOT NULL PRIMARY KEY,
   name VARCHAR NOT NULL,
   email VARCHAR(30) UNIQUE NOT NULL,
   phone_number NUMERIC(10,0) UNIQUE,
   bank_acc_num NUMERIC(17,0) NOT NULL
);

CREATE TABLE BOOK (
    isbn NUMERIC(13,0) NOT NULL PRIMARY KEY,
    title VARCHAR NOT NULL,
    page_count INT,
    price FLOAT NOT NULL,
    num_sold INT,
    num_sold_last_month INT,
    percent_for_publisher FLOAT NOT NULL,
    wholesale_price FLOAT NOT NULL,
    in_stock INT NOT NULL,
    publisher_id CHAR(10) NOT NULL,
    FOREIGN KEY (publisher_id)
                  REFERENCES Publisher(publisher_id)
);

CREATE TABLE ADDRESS (
    street_num INT NOT NULL,
    street VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    province CHAR(2) NOT NULL,
    country VARCHAR(30) NOT NULL,
    postal_code CHAR(6) NOT NULL,
    PRIMARY KEY (street_num, street, postal_code)
);

CREATE TABLE ORDERS (
    order_num NUMERIC(5,0) NOT NULL PRIMARY KEY,
    postal_code CHAR(6) NOT NULL,
    street VARCHAR NOT NULL,
    street_num INT NOT NULL,
    current_city VARCHAR NOT NULL,
    eta DATE,
    FOREIGN KEY (postal_code, street, street_num)
                REFERENCES Address(postal_code, street, street_num)
);

CREATE TABLE AUTHOR (
    author_id CHAR(10) NOT NULL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR NOT NULL
);

CREATE TABLE CREDIT_CARD (
    card_num NUMERIC(16,0) NOT NULL PRIMARY KEY,
    expiry_date DATE NOT NULL,
    cvv NUMERIC(3,0) NOT NULL
);

CREATE TABLE ACCOUNT (
    username VARCHAR NOT NULL PRIMARY KEY,
    password VARCHAR NOT NULL
);

CREATE TABLE GENRE (
    name VARCHAR NOT NULL PRIMARY KEY
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
    genre VARCHAR NOT NULL,
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
    account_name VARCHAR NOT NULL,
    credit_card NUMERIC(16,0) NOT NULL,
    PRIMARY KEY (account_name, credit_card),
    FOREIGN KEY (account_name)
                REFERENCES Account(username),
    FOREIGN KEY (credit_card)
                REFERENCES Credit_Card(card_num)
);

CREATE TABLE SHIPS_TO (
    account_name VARCHAR NOT NULL,
    postal_code CHAR(6) NOT NULL,
    street VARCHAR NOT NULL,
    street_num INT NOT NULL,
    PRIMARY KEY (account_name, postal_code, street, street_num),
    FOREIGN KEY (account_name)
                REFERENCES Account(username),
    FOREIGN KEY (postal_code, street, street_num)
                REFERENCES Address(postal_code, street, street_num)
);

INSERT INTO PUBLISHER (publisher_id, name, email, phone_number, bank_acc_num)
VALUES
    ('abcdefghij', 'Penguin Books', 'penguin@gmail.com', 1234567890, 12345678901234567),
    ('bcdefghijk', 'Not Penguin Books', 'notapenguin@gmail.com', 1234567891, 12345678901234568),
    ('theoldbard', 'Shakespeare Simplified', 'shake@gmail.com', 1234567895, 12345678901234569);

INSERT INTO BOOK  (isbn, title, page_count, price, num_sold, num_sold_last_month, percent_for_publisher, wholesale_price, in_stock, publisher_id)
VALUES
    (1234567890123, 'Murder On The Rue Morgue', 265, 12.99, 2, 1, 30, 5.99, 1, 'abcdefghij'),
    (0987654321098, 'Don Quixote', 450, 15.49, 5, 2, 35, 6.99, 5, 'abcdefghij'),
    (2468013579123, 'Oliver Twist', 1000, 25.00, 1, 0, 20, 10.00, 5, 'bcdefghijk'),
    (1357924680123, 'Othello', 300, 35.00, 10, 1, 40, 20.00, 5, 'theoldbard'),
    (1357924680124, 'Merchant of Venice', 350, 35.00, 18, 1, 40, 20.00, 5, 'theoldbard'),
    (1357924680122, 'Romeo and Juliet', 375, 35.00, 5, 4, 40, 20.00, 1, 'theoldbard');

INSERT INTO ADDRESS (street_num, street, city, province, country, postal_code)
VALUES
    (365, 'Rosewood Ave.', 'Ottawa', 'ON', 'Canada', 'K1R123'),
    (123, 'Something St.', 'Brampton', 'ON', 'Canada', 'L6Z123'),
    (456, 'Hamilton Rd.', 'Cochrane', 'AB', 'Canada', 'T3A123');

INSERT INTO ORDERS (order_num, postal_code, street, street_num, current_city, eta)
VALUES
    (12345, 'K1R123', 'Rosewood Ave.', 365, 'Mississauga', '2022-12-24'),
    (12346, 'T3A123', 'Hamilton Rd.', 456, 'Calgary', NULL),
    (12347, 'L6Z123', 'Something St.', 123, 'Toronto', NULL);

INSERT INTO AUTHOR (author_id, first_name, last_name)
VALUES
    ('shakespear', 'William', 'Shakespeare'),
    ('translates', NULL, 'Translation Corp.'),
    ('mysterywri', 'Edgar', 'Poe'),
    ('oldspanish', 'Miguel', 'Cervantes'),
    ('longwinded', 'Charles', 'Dickens');

INSERT INTO CREDIT_CARD (card_num, expiry_date, cvv)
VALUES
    (1111111111111111, '2025-07-03', 123),
    (2222222222222222, '2024-02-01', 456),
    (1234567890123456, '2023-08-21', 234);

INSERT INTO ACCOUNT (username, password)
VALUES
    ('booklvr', 'ilovebooks1'),
    ('booklvr2', 'ilovebooks1'),
    ('ineedbooks', 'penguins');

INSERT INTO GENRE (name)
VALUES
    ('Mystery'),
    ('Classic'),
    ('Spanish'),
    ('Romance'),
    ('Suspense'),
    ('Sci-Fi'),
    ('Young Adult'),
    ('Nonfiction');

INSERT INTO WRITTEN_BY (book_isbn, author_id)
VALUES
    (0987654321098, 'oldspanish'),
    (1234567890123, 'mysterywri'),
    (2468013579123, 'longwinded'),
    (1357924680123, 'shakespear'),
    (1357924680124, 'shakespear'),
    (1357924680122, 'shakespear'),
    (1357924680123, 'translates'),
    (1357924680124, 'translates'),
    (1357924680122, 'translates'),
    (0987654321098, 'translates');

INSERT INTO HAS_GENRE (book_isbn, genre)
VALUES
    (1234567890123, 'Mystery'),
    (0987654321098, 'Spanish'),
    (0987654321098, 'Classic'),
    (2468013579123, 'Classic'),
    (1357924680123, 'Classic'),
    (1357924680123, 'Suspense'),
    (1357924680124, 'Classic'),
    (1357924680124, 'Suspense'),
    (1357924680124, 'Romance'),
    (1357924680122, 'Classic'),
    (1357924680122, 'Romance');

INSERT INTO INCLUDES (order_num, book_isbn)
VALUES
    (12345, 1234567890123),
    (12345, 0987654321098),
    (12345, 2468013579123),
    (12346, 2468013579123),
    (12347, 1357924680122),
    (12347, 1357924680123);

INSERT INTO PAID_WITH (card_num, order_num)
VALUES
    (1111111111111111, 12345),
    (2222222222222222, 12346),
    (1234567890123456, 12347);

INSERT INTO CHARGES_TO (account_name, credit_card)
VALUES
    ('booklvr', 1111111111111111),
    ('booklvr2', 2222222222222222),
    ('ineedbooks', 1234567890123456);

INSERT INTO SHIPS_TO (account_name, postal_code, street, street_num)
VALUES
    ('booklvr', 'K1R123', 'Rosewood Ave.', 365);
