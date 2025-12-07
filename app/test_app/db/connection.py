# connection.py
import pymysql
import pymysql.cursors
from tkinter import messagebox

# Configuration (Update this)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "1234",
    "database": "hospital"
}

def get_connection():
    """Returns a new MySQL connection or None if an error occurs."""
    try:
        return pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["passwd"],
            database=DB_CONFIG["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect to MySQL: {e}")
        return None
