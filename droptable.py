import mysql.connector
from mysql.connector import Error

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host='127.0.0.1',         # Replace with your database host
        user='root',     # Replace with your database username
        password='', # Replace with your database password
        database='bsc'  # Replace with your database name
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # SQL query to drop the table
        drop_table_query = "DROP TABLE IF EXISTS your_table_name;"  # Replace with your table name
        
        # Execute the query
        cursor.execute(drop_table_query)
        connection.commit()
        
        print("Table dropped successfully.")
        
except Error as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
