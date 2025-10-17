import mysql.connector
from country_operations import fetch_countries


def show_continents(cursor):
    # Query to retrieve all columns from the continents table
    query = "SELECT * FROM continents"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows (continent data)
    continent_data = cursor.fetchall()

    # Display the content of the continents table
    print("population_db Database - Continents Table:")
    print("+----+-----------------------+------------+")
    print("| id | name                  | short_name |")
    print("+----+-----------------------+------------+")
    for row in continent_data:
        print(f"| {row[0]:<2} | {row[1]:<21} | {row[2]:<10} |")
    print("+----+-----------------------+------------+")


def select_continent(cursor):
    try:
        # Show the content of the continents table
        show_continents(cursor)

        # Prompt the user to select a continent
        continent_input = input("Enter the short name, name, or id of the continent: ")

        # Fetch the continent data based on user input
        query = "SELECT * FROM continents WHERE short_name = %s OR name = %s OR id = %s"
        cursor.execute(query, (continent_input, continent_input, continent_input))
        continent_data = cursor.fetchone()

        if continent_data:
            continent_name = continent_data[1]
            continent_short_name = continent_data[2]
            print(f"Continent name is: {continent_name}, short name is: {continent_short_name}.")
            fetched_countries = fetch_countries(continent_name)
            return continent_name, continent_short_name, fetched_countries  # Return the name of the selected continent
        else:
            print("Continent not found.")
            return None

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None