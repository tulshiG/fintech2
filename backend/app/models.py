import mysql.connector
from app.database import get_db_connection

def create_users_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()

# Ensure the table exists on startup
create_users_table()
