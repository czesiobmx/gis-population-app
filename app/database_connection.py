import mysql.connector
import os


def establish_connection():
    # Establish a connection to MySQL
    conn = mysql.connector.connect(
        host="mysql-db",
        port=3306,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    cursor.close()
    conn.close()