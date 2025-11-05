import mysql.connector

# 🔹 Configure your MySQL credentials here
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # your MySQL username
    "password": "Mayank@14#",  # your MySQL password
    "database": "inventory_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100),
            category VARCHAR(100),
            price FLOAT,
            quantity INT,
            expiry_days INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sort_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            algorithm VARCHAR(50),
            time_taken FLOAT,
            record_count INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100),
            predicted_label VARCHAR(50),
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def insert_inventory(name, category, price, qty, expiry_days):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (product_name, category, price, quantity, expiry_days)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, category, price, qty, expiry_days))
    conn.commit()
    conn.close()

def get_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, category, price, quantity, expiry_days FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_sort_log(algorithm, time_taken, record_count):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sort_logs (algorithm, time_taken, record_count)
        VALUES (%s, %s, %s)
    """, (algorithm, time_taken, record_count))
    conn.commit()
    conn.close()
