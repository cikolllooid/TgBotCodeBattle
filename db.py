# db.py
import psycopg2
from config import *

def get_connection():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    conn.autocommit = True
    return conn
