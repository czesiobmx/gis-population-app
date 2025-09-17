from database_connection import *
from database_functions import insert_into_table
from continent_operations import select_continent
from country_operations import *
from population_insert import create_and_insert_population
from folium_markers_map import markers_execute
from folium_choropleth_map import choropleth_execute
from folium_merge_maps import merge_execute
from dotenv import load_dotenv


# load env vars once app starts
load_dotenv()


def main_menu():
    print("\nMain Menu:")
    print("1. Create continents table in MySQL and insert considered continent data")
    print("2. Select continent to work with")
    print("3. Show selected continent's countries")
    print("4. Fetch population of selected continent's countries for a given year")
    print("5. Create countries_population table and insert population data")
    print("6. Save population as CSV, create population graph and folium markers map")
    print("7. Save GeoJSON and create folium choropleth map")
    print("8. Generate interactive folium map")
    print("9. Exit")


if __name__ == "__main__":
    conn, cursor = establish_connection() # using database_connection.py
    selected_continent = None
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            insert_into_table(conn,cursor) # using database_functions.py

        elif choice == '2':
            selected_continent = select_continent(cursor) # using continent_operations.py
            if selected_continent:
                print("Selected continent:", selected_continent[0])

        elif choice == '3':
            if selected_continent:
                show_countries(selected_continent[2]) # using country_operations.py
            else:
                print("No continent selected. Please select a continent first.")

        elif choice == '4':
            if selected_continent:
                year = input("Enter the year: ")
                country_data, year = fetch_population(selected_continent[2], year) # using country_operations.py
            else:
                print("No continent selected. Please select a continent first.")

        elif choice == '5':
            if selected_continent:
                if 'country_data' in locals():
                    create_and_insert_population(country_data, year, selected_continent[1], cursor, conn) # using population_insert.py 
                else:
                    print("No population data fetched. Please fetch population data first.")
            else:
                print("No continent selected. Please select a continent first.")

        elif choice == '6':
            markers_execute(cursor) # using folium_markers_map.py

        elif choice == '7':
            choropleth_execute() # using folium_choropleth_map.py

        elif choice == '8':
            merge_execute(cursor) # using folium_merge_maps.py

        elif choice == '9':
            print("Exit")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")
    close_connection(conn, cursor) # using database_connection.py