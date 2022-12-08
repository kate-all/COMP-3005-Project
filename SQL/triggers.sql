-- Decrease stock and increase sales data each time a book is ordered
CREATE FUNCTION reduce_inventory()
    returns TRIGGER
    language plpgsql
    AS $reduce_inventory$
begin
    UPDATE Book
    SET in_stock = (
                       SELECT in_stock
                       FROM Book
                       WHERE isbn = NEW.book_isbn
                   ) - 1,
        num_sold = (
                        SELECT num_sold
                        FROM Book
                        WHERE isbn = NEW.book_isbn
                    ) + 1,
        num_sold_last_month = (
                        SELECT num_sold_last_month
                        FROM Book
                        WHERE isbn = NEW.book_isbn
                    ) + 1

    WHERE isbn = NEW.book_isbn;

    RETURN NEW;
end;
$reduce_inventory$

CREATE TRIGGER reduce_inventory
    BEFORE INSERT
    ON Includes
    FOR EACH ROW
    EXECUTE PROCEDURE reduce_inventory();

-- Add reorder data to temp table
-- In reality, I'd use a module to send emails, so this table would not
-- exist. For the purposes of the project, I'm creating this table so the employee
-- can see what needs to be reordered. Thus this is not part of the database schema
-- for this project.
CREATE TABLE REORDER (
    publisher_email VARCHAR(30) NOT NULL,
    book_isbn NUMERIC(13,0) NOT NULL,
    reorder_quantity INTEGER NOT NULL,
    PRIMARY KEY (publisher_email, book_isbn, reorder_quantity)
);

CREATE FUNCTION reorder()
    returns TRIGGER
    language plpgsql
    AS $reorder$
begin
    IF NEW.in_stock = 0 THEN
        INSERT INTO Reorder (book_isbn, reorder_quantity, publisher_email)
        VALUES (
                NEW.isbn,
                NEW.num_sold_last_month,
                (SELECT email FROM Publisher
                    WHERE NEW.publisher_id = Publisher.Publisher_id
                )
        );
    END IF;

RETURN NEW;
end;
$reorder$

CREATE TRIGGER reorder
    BEFORE UPDATE
    ON Book
    FOR EACH ROW
    EXECUTE PROCEDURE reorder();
