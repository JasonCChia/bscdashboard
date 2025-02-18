import mysql.connector
from config import Config

def create_connection():
    try:
        print("Attempting database connection with:")
        print(f"Host: {Config.DB_HOST}")
        print(f"User: {Config.DB_USER}")
        print(f"Database: {Config.DB_NAME}")
        
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        raise