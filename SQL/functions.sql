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