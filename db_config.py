import mysql.connector
from mysql.connector import Error

config={
    'user': 'root',
    'password': 'Test@1234',
    'host': 'localhost',
    'database': 'scraped_data'
}

def get_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

