import psycopg2
from psycopg2 import OperationalError


def execute_query(cur, query):
    try:
        cur.execute(query)
    except OperationalError as e:
        print("ERROR:\n", e)

def create_tables(cur):
    f = open("./SQL/init.sql", "r").read().split("\n")

    book_query = "".join(f[3:15])

    execute_query(cur, book_query)

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
