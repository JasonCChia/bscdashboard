import mysql.connector

def modify_table():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="bsc"  # Replace with your database name
    )

    cursor = connection.cursor()

    # List of new columns to add
    new_columns = {
        "measurement": "VARCHAR(50)",
        "issues": "VARCHAR(255)",
        "implication": "VARCHAR(255)",
        "action": "VARCHAR(255)",
        "accountabilities": "VARCHAR(255)"
    }

    for column, data_type in new_columns.items():
        # Check if the column already exists
        check_column_query = f"""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'objective_note' AND COLUMN_NAME = '{column}'
        """
        cursor.execute(check_column_query)
        result = cursor.fetchone()

        if not result:
            # Add column if it does not exist
            alter_table_query = f"ALTER TABLE objective_note ADD COLUMN {column} {data_type}"
            cursor.execute(alter_table_query)
            print(f"Column '{column}' added successfully.")
        else:
            print(f"Column '{column}' already exists.")

    # Add foreign key constraint for `measurement`
    try:
        cursor.execute("""
        ALTER TABLE objective_note 
        ADD CONSTRAINT fk_measurement FOREIGN KEY (measurement) 
        REFERENCES measurement(id) ON DELETE SET NULL
        """)
        print("Foreign key constraint for 'measurement' added successfully.")
    except mysql.connector.Error as err:
        print(f"Foreign key might already exist or error occurred: {err}")

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    modify_table()
