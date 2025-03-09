import mysql.connector
from datetime import datetime

def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="bsc"  # Replace with your database name
    )

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    
    user_table = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50),
        horizon SMALLINT,
        objective JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )"""
    
    initiative_table = """
    CREATE TABLE IF NOT EXISTS initiative (
        id INT AUTO_INCREMENT PRIMARY KEY,
        initiative_name VARCHAR(255) NOT NULL,
        objective VARCHAR(255),
        target VARCHAR(255),
        achieved VARCHAR(255),
        status VARCHAR(50),
        start_date DATE,
        end_date DATE,
        note VARCHAR(255),
        created_by INT,
        updated_by INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE SET NULL,
        FOREIGN KEY (updated_by) REFERENCES user(id) ON DELETE SET NULL
    )"""
    
    measurement_table = """
    CREATE TABLE IF NOT EXISTS measurement (
        id INT AUTO_INCREMENT PRIMARY KEY,
        measurement_name VARCHAR(255) NOT NULL,
        objective VARCHAR(255),
        target INT,
        achieved INT,
        created_by INT,
        updated_by INT,
        note VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE SET NULL,
        FOREIGN KEY (updated_by) REFERENCES user(id) ON DELETE SET NULL
    )"""
    
    log_activity_table = """
    CREATE TABLE IF NOT EXISTS log_activity (
        id INT AUTO_INCREMENT PRIMARY KEY,
        table_name VARCHAR(50) NOT NULL,
        action VARCHAR(50) NOT NULL,
        record_id INT NOT NULL,
        user_id INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
    )"""
    
    objective_note_table = """
    CREATE TABLE IF NOT EXISTS objective_note (
        id INT AUTO_INCREMENT PRIMARY KEY,
        objective VARCHAR(255),
        measurement_id INT, 
        note TEXT NOT NULL,
        issues TEXT,
        implication TEXT,
        action TEXT,
        accountabilities TEXT,
        created_by INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES user(id) ON DELETE SET NULL
    )"""
    
    cursor.execute(user_table)
    cursor.execute(initiative_table)
    cursor.execute(measurement_table)
    cursor.execute(log_activity_table)
    cursor.execute(objective_note_table)
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
