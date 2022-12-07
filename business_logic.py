import psycopg2
from psycopg2 import OperationalError
import random

def execute_query(cur, query):
    try:
        cur.execute(query)
    except OperationalError as e:
        print("ERROR:\n", e)

def login(cur, user, password):
    cur.execute(""" SELECT * FROM Account
    WHERE username = %s AND
    password = %s;
    """, (user, password))

    if cur.fetchall() == []:
        return False

    return True

def get_addresses(cur, user):
    cur.execute("""SELECT (street_num, street, postal_code) FROM Ships_To WHERE account_name=%s""",(user,))
    return cur.fetchall()

def get_cards(cur, user):
    cur.execute("""SELECT credit_card FROM Charges_To WHERE account_name=%s""", (user,))
    return cur.fetchall()

def get_order(cur, order_num):
    cur.execute("""SELECT * FROM Orders WHERE Orders.order_num=%s""", (order_num,))
    return cur.fetchone()

def is_valid_username(cur, user):
    cur.execute("""SELECT * FROM Account
    WHERE username = %s;
    """, (user,))

    if cur.fetchall() == []:
        return True
    return False

def create_new_account(cur, user, password):
    try:
        cur.execute("INSERT INTO Account (username, password) VALUES (%s, %s);", (user, password))
    except OperationalError as e:
        print("ERROR", e)
        return False

    return True

def add_card(cur, card_num, expiry_date, cvv, user):
    # Add card to credit cards if new
    cur.execute("""SELECT * FROM Credit_Card WHERE card_num=%s;""", (card_num,))
    if cur.fetchall() == []:
        cur.execute("""INSERT INTO Credit_Card (card_num, expiry_date, cvv) 
        VALUES (%s, TO_DATE(%s, 'YYYY-MM-DD'), %s);
        """, (card_num, expiry_date, cvv))

    # Link card to account if not linked already
    cur.execute("""SELECT * FROM Charges_To WHERE account_name=%s AND credit_card=%s""", (user, card_num))
    cur.execute("""INSERT INTO Charges_To (account_name, credit_card) 
    VALUES (%s, %s);""", (user, card_num))

def add_address(cur, street_num, street, city, province, country, postal_code, user):
    # Add address to addresses if new
    cur.execute("""SELECT * FROM Address WHERE street_num=%s AND street=%s AND postal_code=%s""", (street_num, street, postal_code))
    if cur.fetchall() == []:
        cur.execute("""INSERT INTO Address (street_num, street, city, province, country, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s)""", (street_num, street, city, province, country, postal_code))

    # Link address to account if not linked already
    cur.execute("""SELECT * FROM Ships_To WHERE account_name=%s AND postal_code=%s AND street=%s AND street_num=%s""",
                (user, postal_code, street, street_num))
    if cur.fetchall() == []:
        cur.execute("""INSERT INTO Ships_To 
        VALUES (%s, %s, %s, %s)""", (user, postal_code, street, street_num))

def create_order(cur, postal_code, street, street_num, basket, card):
    order_num = "".join([str(random.randint(0,9)) for i in range(0,5)])
    cur.execute("""INSERT INTO Orders (order_num, postal_code, street, street_num, current_city, eta)
    VALUES (%s, %s, %s, %s, 'Mississauga', NULL)""", (order_num, postal_code, street, street_num))

    for book in basket:
        cur.execute("""INSERT INTO Includes 
        VALUES (%s, %s)""", (order_num, book))

    cur.execute("""INSERT INTO Paid_With 
    VALUES (%s, %s)""",(card, order_num))

    return order_num

def get_book(cur, isbn, user_type):
    if user_type == 'c':
        cur.execute("""SELECT (isbn, title, first_name, last_name, genre, page_count, price, name)
                        FROM Book, Written_By, Author, Publisher, Has_Genre
                        WHERE Book.isbn = Written_By.book_isbn AND
                            Written_By.author_id = Author.author_id AND
                            Book.publisher_id = Publisher.publisher_id AND
                            Book.isbn = Has_Genre.book_isbn AND
                            Book.isbn = %s
                    """, (isbn,))

    else:
        cur.execute("""SELECT (isbn, title, first_name, last_name, genre, page_count, price, name, num_sold, num_sold_last_month, percent_for_publisher, wholesale_price, in_stock)
                        FROM Book, Written_By, Author, Publisher, Has_Genre
                        WHERE Book.isbn = Written_By.book_isbn AND
                            Written_By.author_id = Author.author_id AND
                            Book.publisher_id = Publisher.publisher_id AND
                            Book.isbn = Has_Genre.book_isbn AND
                            Book.isbn = %s
                    """, (isbn,))

    return cur.fetchone()

def is_available(cur, isbn):
    cur.execute("""SELECT * FROM Book WHERE isbn=%s AND in_stock > 0""", (isbn,))
    return cur.fetchall() != []

def get_publisher(cur, p_name):
    cur.execute("""SELECT publisher_id FROM Publisher WHERE name=%s""", (p_name, ))
    return cur.fetchall()

def add_publisher(cur, p_name, p_email, p_phone_num, p_bank_acc):
    id = "".join([str(random.randint(0,9)) for i in range(0,10)])
    cur.execute("""INSERT INTO Publisher 
    VALUES (%s, %s, %s, %s, %s)""", (id, p_name, p_email, p_phone_num, p_bank_acc))
    return id

def add_book(cur, isbn, title, page_count, price, price_wholesale, in_stock, percent_for_publisher, p_id, author_names, genres):
    # Add Book
    search(cur, "isbn", isbn)
    if cur.fetchall() != []:
        return False

    cur.execute("""INSERT INTO Book (isbn, title, page_count, price, wholesale_price, in_stock, percent_for_publisher, publisher_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (isbn, title, page_count, price, price_wholesale, in_stock, percent_for_publisher, p_id))

    # Add Genres
    for name in genres:
        cur.execute("""SELECT name FROM Genre WHERE name=%s""", (name,))
        if cur.fetchall() == []:
            cur.execute("""INSERT INTO Genre VALUES (%s)""", (name,))
        cur.execute("""INSERT INTO Has_Genre VALUES (%s, %s)""", (isbn, name))

    # Add Authors
    for author in author_names:
        name = author.split(" ")
        cur.execute("""SELECT author_id FROM Author WHERE first_name=%s AND last_name=%s""", (name[0], name[1]))
        id = cur.fetchall()
        if id == []:
            id = "".join([str(random.randint(0,9)) for i in range(0,10)])
            cur.execute("""INSERT INTO Author VALUES (%s, %s, %s)""", (id, name[0], name[1]))
        else:
            id = id[0]

        cur.execute("""INSERT INTO Written_By VALUES (%s, %s)""", (isbn, id))

    return True

def delete_book(cur, isbn):
    cur.execute("""SELECT publisher_id FROM Book WHERE isbn=%s""",(isbn,))
    p_id = cur.fetchall()

    if p_id == []:
        return False

    # Remove Author if needed
    cur.execute("""SELECT author_id FROM Written_By WHERE book_isbn=%s""",(isbn,))
    author_ids = cur.fetchall()
    for author in author_ids:
        cur.execute("""SELECT * FROM Written_By WHERE author_id=%s""",(author,))
        if len(cur.fetchall()):
            cur.execute("""DELETE FROM Written_By WHERE author_id=%s""",(author,))
            cur.execute("""DELETE FROM Author WHERE author_id=%s""",(author,))

    # Remove from Has_Genre
    cur.execute("""DELETE FROM Has_Genre WHERE book_isbn=%s""",(isbn,))

    # Remove Book
    cur.execute("""DELETE FROM Book WHERE isbn=%s""", (isbn,))

    # Remove publisher if no longer participating in relation
    p_id = p_id[0]
    cur.execute("""SELECT isbn FROM Book WHERE publisher_id=%s""",(p_id,))
    if len(cur.fetchall()) == 0: # This publisher hasn't published any other books
        cur.execute("""DELETE FROM Publisher WHERE publisher_id=%s""",(p_id,))

    return True

def search(cur, field, val):
    try:
        if field == "title":
            val = " ".join(val)
            cur.execute("SELECT (isbn, title) FROM Book WHERE title=%s;", (val,))

        elif field == "isbn":
            cur.execute("SELECT (isbn, title) FROM Book WHERE isbn=%s;", (val,))

        elif field == "price":
            if val[0] == "<":
                cur.execute("SELECT (isbn, title) FROM Book WHERE price < %s;", (val[1],))

            elif val[0] == ">":
                cur.execute("SELECT (isbn, title) FROM Book WHERE price > %s;", (val[1],))

            else:
                cur.execute("SELECT (isbn, title) FROM Book WHERE price = %s;", (val[1],))

        elif field == "page_count":
            if val[0] == "<":
                cur.execute("SELECT (isbn, title) FROM Book WHERE page_count < %s;", (val[1],))

            elif val[0] == ">":
                cur.execute("SELECT (isbn, title) FROM Book WHERE page_count > %s;", (val[1],))

            else:
                cur.execute("SELECT (isbn, title) FROM Book WHERE page_count = %s;", (val[1],))

        elif field == "genre":
           cur.execute("""
                SELECT (isbn, title)
                FROM Book, Has_Genre
                WHERE Book.isbn = Has_Genre.book_isbn AND
                    Has_Genre.genre = %s;
                """, (val[0],))

        elif field == "author":
            cur.execute("""
                SELECT (isbn, title)
                FROM Book, Written_By, Author 
                WHERE Book.isbn = Written_by.book_isbn AND
                    Written_by.author_id = Author.author_id AND
                    Author.last_name = %s;
                """, (" ".join(val),))

        elif field == "publisher":
            cur.execute("""
                SELECT (isbn, title)
                FROM Book, Publisher 
                WHERE Book.publisher_id = Publisher.publisher_id AND
                    publisher.name = %s;
                """, (" ".join(val),))

        elif field == "available":
            cur.execute("SELECT (isbn, title) FROM Book WHERE in_stock > 0;")

        else:
            return None

    except OperationalError as e:
        print("SEARCH ERROR:\n", e)

    return cur.fetchall()

def create_tables(cur):
    f = open("./SQL/init.sql", "r").read().split("\n")

    publisher_query = "".join(f[3:10])
    execute_query(cur, publisher_query)

    book_query = "".join(f[11:25])
    execute_query(cur, book_query)

    address_query = "".join(f[26:35])
    execute_query(cur, address_query)

    order_query = "".join(f[36:46])
    execute_query(cur, order_query)

    author_query = "".join(f[47:52])
    execute_query(cur, author_query)

    credit_card_query = "".join(f[53:58])
    execute_query(cur, credit_card_query)

    account_query = "".join(f[59:63])
    execute_query(cur, account_query)

    genre_query = "".join(f[64:67])
    execute_query(cur, genre_query)

    written_by_query = "".join(f[68:77])
    execute_query(cur, written_by_query)

    has_genre_query = "".join(f[78:87])
    execute_query(cur, has_genre_query)

    includes_query = "".join(f[88:97])
    execute_query(cur, includes_query)

    paid_with_query = "".join(f[98:107])
    execute_query(cur, paid_with_query)

    charges_to_query = "".join(f[108:117])
    execute_query(cur, charges_to_query)

    ships_to_query = "".join(f[118:129])
    execute_query(cur, ships_to_query)


def add_dummy_data(cur):
    f = open("./SQL/init.sql", "r").read().split("\n")

    publisher_data = "".join(f[130:135])
    execute_query(cur, publisher_data)

    book_data = "".join(f[136:144])
    execute_query(cur, book_data)

    address_data = "".join(f[145:150])
    execute_query(cur, address_data)

    orders_data = "".join(f[151:156])
    execute_query(cur, orders_data)

    author_data = "".join(f[157:164])
    execute_query(cur, author_data)

    credit_card_data = "".join(f[165:170])
    execute_query(cur, credit_card_data)

    account_data = "".join(f[171:176])
    execute_query(cur, account_data)

    genre_data = "".join(f[177:187])
    execute_query(cur, genre_data)

    written_by_data = "".join(f[188:200])
    execute_query(cur, written_by_data)

    has_genre_data = "".join(f[201:214])
    execute_query(cur, has_genre_data)

    includes_data = "".join(f[215:223])
    execute_query(cur, includes_data)

    paid_with_data = "".join(f[224:229])
    execute_query(cur, paid_with_data)

    charges_to_data = "".join(f[230:235])
    execute_query(cur, charges_to_data)

    ships_to_data = "".join(f[236:239])
    execute_query(cur, ships_to_data)

def connect_to_db():
    con = psycopg2.connect(
        database="LookInnaBook",
        user="postgres",
        password="3005proj")

    con.autocommit = True
    return con.cursor()


def create_database():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="3005proj",
        host="127.0.0.1",
        port="5432"
    )

    con.autocommit = True
    cur = con.cursor()

    drop_query = "DROP DATABASE IF EXISTS \"LookInnaBook\";"
    execute_query(cur, drop_query)

    create_query = "CREATE DATABASE \"LookInnaBook\";"
    execute_query(cur, create_query)

    cur = connect_to_db()

    create_tables(cur)
    add_dummy_data(cur)

    return cur
