import sqlite3
import hashlib

# Database Setup
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Authentication
def verify_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# User Creation
def create_user(username, name, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)", (username, name, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists