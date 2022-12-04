DROP DATABASE IF EXISTS "LookInnaBook";
CREATE DATABASE "LookInnaBook";

CREATE TABLE BOOK (
    isbn NUMERIC(13,0) NOT NULL PRIMARY KEY,
    title VARCHAR NOT NULL,
    page_count INT,
    price NUMERIC(4,2),
    num_sold INT,
    num_sold_last_month INT,
    percent_for_publisher NUMERIC(3,2),
    wholesale_price NUMERIC(4,2),
    publisher_id CHAR(10)
)

