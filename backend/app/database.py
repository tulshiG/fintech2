import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def get_db_connection():
    """Connects to MySQL database."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def create_user(pan_no, username, hashed_password):
    """Registers a new user with hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (pan_no, username, hashed_password) VALUES (%s, %s, %s)",
        (pan_no, username, hashed_password)
    )
    conn.commit()
    conn.close()

def get_user_by_pan(pan_no):
    """Fetches user by PAN number."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE pan_no = %s", (pan_no,))
    user = cursor.fetchone()
    conn.close()
    return user
