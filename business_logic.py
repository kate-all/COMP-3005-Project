import psycopg2
from psycopg2 import OperationalError


def execute_query(cur, query):
    try:
        cur.execute(query)
    except OperationalError as e:
        print("ERROR:\n", e)

def login(cur, user, password):
    return

def search(cur, field, val):
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
