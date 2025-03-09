import mysql.connector
from mysql.connector import Error

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host='127.0.0.1',         # Replace with your database host
        user='root',     # Replace with your database username
        password=''  # Replace with your database password
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # SQL query to drop the database
        drop_database_query = "DROP DATABASE IF EXISTS bsc;"  # Replace with your database name
        
        # Execute the query
        cursor.execute(drop_database_query)
        connection.commit()
        
        print("Database dropped successfully.")
        
except Error as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")