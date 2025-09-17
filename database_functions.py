from database_connection import *
import mysql.connector


def create_continents_table(cursor):
    # Create the continents table if it doesn't exist
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS continents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            short_name VARCHAR(100)
        );
    """
    cursor.execute(create_table_query)


def get_existing_databases(cursor):
    # Query to retrieve existing databases
    query = "SHOW DATABASES"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows (database names)
    existing_databases = [row[0] for row in cursor.fetchall()]

    return existing_databases


def get_existing_tables(cursor, database):
    # Query to retrieve existing tables in the specified database
    query = f"SHOW TABLES IN {database}"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows (table names)
    existing_tables = [row[0] for row in cursor.fetchall()]

    return existing_tables


def get_existing_columns(cursor, table_name):
    # Query to retrieve existing column names from the specified table
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows (column names)
    existing_columns = [row[0] for row in cursor.fetchall()]

    return existing_columns


def insert_into_table(conn, cursor):  

    # Establish a connection to MySQL
    try:
        # Create continents table
        create_continents_table(cursor)
        print("Continents table created successfully or already exists.")

        # Show existing databases
        existing_databases = get_existing_databases(cursor)
        print("Existing databases for root user:", existing_databases)

        # Prompt the user for database name
        database = input("Enter MySQL database: ")

        # Show existing tables in the selected database
        existing_tables = get_existing_tables(cursor, database)
        print(f"Existing tables in '{database}':", existing_tables)

        # Prompt the user for table name
        table_name = input("Enter table name: ")

        # Retrieve existing column names from the specified table
        existing_columns = get_existing_columns(cursor, table_name)
        print("Existing column names in the selected table:", existing_columns)

        # Prompt the user to enter values for existing columns (excluding the 'id' column)
        values = []
        for column in existing_columns:
            if column.lower() != 'id':  # Exclude the 'id' column (case-insensitive comparison)
                value = input(f"Enter value for {column}: ")
                values.append(value)

        # Build the SQL INSERT INTO statement
        columns_str = ', '.join([column for column in existing_columns if
                                 column.lower() != 'id'])  # Exclude the 'id' column (case-insensitive comparison)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        # Execute the SQL statement
        cursor.execute(query, values)
        conn.commit()

        print("Data inserted successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")