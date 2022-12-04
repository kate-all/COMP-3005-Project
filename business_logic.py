import psycopg2
from psycopg2 import OperationalError


def execute_query(cur, query):
    try:
        cur.execute(query)
    except OperationalError as e:
        print("ERROR:\n", e)


def create_tables(cur):
    f = open("./SQL/init.sql", "r").read().split("\n")

    publisher_query = "".join(f[3:10])
    execute_query(cur, publisher_query)

    book_query = "".join(f[11:24])
    execute_query(cur, book_query)

    address_query = "".join(f[25:34])
    execute_query(cur, address_query)

    order_query = "".join(f[35:45])
    execute_query(cur, order_query)

    author_query = "".join(f[46:51])
    execute_query(cur, author_query)

    credit_card_query = "".join(f[52:57])
    execute_query(cur, credit_card_query)

    account_query = "".join(f[58:62])
    execute_query(cur, account_query)

    genre_query = "".join(f[63:66])
    execute_query(cur, genre_query)

    written_by_query = "".join(f[67:76])
    execute_query(cur, written_by_query)

    has_genre_query = "".join(f[77:86])
    execute_query(cur, has_genre_query)

    includes_query = "".join(f[87:96])
    execute_query(cur, includes_query)

    paid_with_query = "".join(f[97:106])
    execute_query(cur, paid_with_query)

    charges_to_query = "".join(f[107:116])
    execute_query(cur, charges_to_query)

    ships_to_query = "".join(f[117:])
    execute_query(cur, ships_to_query)




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

    con = psycopg2.connect(
        database="LookInnaBook",
        user="postgres",
        password="3005proj")

    con.autocommit = True
    cur = con.cursor()

    create_tables(cur)

    return cur
