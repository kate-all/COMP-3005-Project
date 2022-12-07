-- SEARCHES --
SELECT (isbn, title)
FROM BOOK
WHERE title = 'atitle';

SELECT (isbn, title)
FROM Book
WHERE isbn = isbn;

SELECT (isbn, title)
FROM Book
WHERE page_count < avalue; -- also with > and =

SELECT (isbn, title)
FROM Book
WHERE price < avalue; -- also with > and =

SELECT (isbn, title)
FROM Book, Has_Genre
WHERE Book.isbn = Has_Genre.book_isbn AND
      Has_Genre.genre = 'agenre';

SELECT (isbn, title)
FROM Book, Written_By, Author
WHERE Book.isbn = Written_by.book_isbn AND
        Written_by.author_id = Author.author_id AND
        Author.last_name = 'alastname';

SELECT (isbn, title)
FROM Book, Publisher
WHERE Book.publisher_id = Publisher.publisher_id AND
        publisher.name = 'apublisher';

SELECT (isbn, title) FROM Book WHERE in_stock > 0;

SELECT * FROM Book WHERE isbn=%s AND in_stock > 0

-- VALIDATION --
SELECT * FROM Account
WHERE username = 'ausername';

INSERT INTO Account (username, password) VALUES ('auser', 'apass');

SELECT * FROM Account
WHERE username = 'auser' AND
        password = 'apassword';

-- LOTS OF DETAIL FROM A SINGULAR RECORD
SELECT (isbn, title, first_name, last_name, genre, page_count, price, name)
FROM Book, Written_By, Author, Publisher, Has_Genre
WHERE Book.isbn = Written_By.book_isbn AND
        Written_By.author_id = Author.author_id AND
        Book.publisher_id = Publisher.publisher_id AND
        Book.isbn = Has_Genre.book_isbn AND
        Book.isbn = 1111111111111

SELECT (isbn, title, first_name, last_name, genre, page_count, price, name, num_sold, num_sold_last_month, percent_for_publisher, wholesale_price, in_stock)
FROM Book, Written_By, Author, Publisher, Has_Genre
WHERE Book.isbn = Written_By.book_isbn AND
        Written_By.author_id = Author.author_id AND
        Book.publisher_id = Publisher.publisher_id AND
        Book.isbn = Has_Genre.book_isbn AND
        Book.isbn = 1111111111111

-- CREDIT CARD
SELECT * FROM Credit_Card WHERE card_num=%s;

INSERT INTO Credit_Card (card_num, expiry_date, cvv)
VALUES (%s, %s, TO_DATE(%s, 'YYYY-MM-DD'));

SELECT * FROM Charges_To WHERE account_name=%s AND credit_card=%s

INSERT INTO Charges_To (account_name, credit_card)
VALUES (%s, %s);

-- ADDRESS
SELECT * FROM Address WHERE street_num=%s AND street=%s AND postal_code=%s

INSERT INTO Address (street_num, street, city, province, country, postal_code)
VALUES (%s, %s, %s, %s, %s, %s)

SELECT * FROM Ships_To WHERE account_name=%s AND postal_code=%s AND street=%s AND street_num=%s

INSERT INTO Ships_To
VALUES (%s, %s, %s, %s)

SELECT * FROM Ships_To WHERE username=%s

-- ORDER
INSERT INTO Orders (order_num, postal_code, street, street_num, current_city, eta)
VALUES (%s, %s, %s, %s, 'Mississauga', NULL)

INSERT INTO Includes
VALUES (%s, %s)

INSERT INTO Paid_With
VALUES (%s, %s)

SELECT * FROM Orders WHERE Orders.order_num=%s

-- PUBLISHER
INSERT INTO Publisher
VALUES (%s, %s, %s, %s, %s)

-- ADDING BOOKS
INSERT INTO Book (isbn, title, page_count, price, wholesale_price, in_stock, percent_for_publisher, publisher_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

SELECT author_id FROM Author WHERE first_name=%s AND last_name=%s
INSERT INTO Author VALUES (%s, %s, %s)
INSERT INTO Written_By VALUES (%s, %s)

SELECT name FROM Genre WHERE name=%s
INSERT INTO Genre VALUES (%s)
INSERT INTO Has_Genre VALUES (%s, %s)

-- DELETING BOOKS
SELECT publisher_id FROM Book WHERE isbn=%s

SELECT author_id FROM Written_By WHERE book_isbn=%s
SELECT * FROM Written_By WHERE author_id=%s
DELETE FROM Written_By WHERE author_id=%s

DELETE FROM Author WHERE author_id=%s

DELETE FROM Has_Genre WHERE book_isbn=%s

DELETE FROM Book WHERE isbn=%s

SELECT isbn FROM Book WHERE publisher_id=%s
DELETE FROM Publisher WHERE publisher_id=%s

-- REPORT
SELECT sum(num_sold_last_month) FROM Book

SELECT genre, sum(num_sold_last_month) AS sold FROM Book, Has_Genre
WHERE Book.isbn = Has_Genre.book_isbn
GROUP BY genre
ORDER BY sold DESC
LIMIT 1

SELECT genre, sum(num_sold) AS sold FROM Book, Has_Genre
WHERE Book.isbn = Has_Genre.book_isbn
GROUP BY genre
ORDER BY sold DESC
    LIMIT 1
