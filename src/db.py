# src/db.py
import sqlite3

DB_NAME = "inventory.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup_database():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER,
        expiry_days INTEGER
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS sort_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        algorithm TEXT,
        array_size INTEGER,
        time_taken REAL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ai_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        ai_action TEXT,
        prediction TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_inventory(product, category, price, quantity, expiry_days):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO inventory VALUES (NULL, ?, ?, ?, ?, ?)",
              (product, category, price, quantity, expiry_days))
    conn.commit()
    conn.close()

def insert_sort_log(algo, size, time_taken):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO sort_log VALUES (NULL, ?, ?, ?)",
              (algo, size, time_taken))
    conn.commit()
    conn.close()

def insert_ai_prediction(name, action, prediction):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO ai_predictions VALUES (NULL, ?, ?, ?)",
              (name, action, prediction))
    conn.commit()
    conn.close()
