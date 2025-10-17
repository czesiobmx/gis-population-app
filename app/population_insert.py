import pycountry
import mysql.connector


def create_population_table(cursor):
    # Create the Countries_population table if it doesn't exist
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS countries_population (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Country VARCHAR(100),
            Year INT,
            Population INT,
            Alpha_2_Code VARCHAR(10),
            Alpha_3_Code VARCHAR(10),
            Continent_Short_Name VARCHAR(10)
        )
    """
    cursor.execute(create_table_query)


def insert_population_data(cursor, country_data, year, continent_short_name):
    try:
        for country, population in country_data.items():
            alpha_2_code = pycountry.countries.get(name=country).alpha_2
            alpha_3_code = pycountry.countries.get(name=country).alpha_3
            # Insert data into the countries_population table
            insert_query = f"""
                INSERT INTO countries_population (Country, Year, Population, Alpha_2_Code, Alpha_3_Code, Continent_Short_Name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (country, year, population, alpha_2_code, alpha_3_code, continent_short_name))
            print(f"Data for {country} in year {year} inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_and_insert_population(country_data, year, continent_short_name, cursor, conn):
    try:
        # Create the Countries_population table
        create_population_table(cursor)

        # Insert population data into the table
        insert_population_data(cursor, country_data, year, continent_short_name)

        conn.commit()
        print("Data inserted successfully into the 'countries_population' table.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")