import psycopg2

def create_connection():
    connection = psycopg2.connect(
        database="LookInnaBook",
        user="postgres",
        password="3005proj")

    return connection.cursor()