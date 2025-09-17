import csv
import folium
import pandas as pd

from folium_choropleth_map import fetch_geojson_for_countries, save_geojson_data
from folium_markers_map import get_population_data, get_country_coordinates, \
    save_population_data_as_csv


def plot_merged_map(population_data, countries):
    # Initialize a map centered at a specific location
    folium_map = folium.Map(location=[0, 0], zoom_start=2)

    # Create a dictionary to store FeatureGroups for each country
    country_marker_groups = {}

    # Generate folium Marker layers
    # Loop through population data and add markers to respective FeatureGroup
    for country, data in population_data.items():
        lat, lon = get_country_coordinates(country)
        if lat is not None and lon is not None:
            popup_content = f"<b>{country}</b><br>"
            for year, population in data.items():
                # Format population with commas as thousands separator
                formatted_population = "{:,}".format(population)
                popup_content += f"<div>{year} - {formatted_population}</div>"
            # Check if FeatureGroup for the country already exists
            if country not in country_marker_groups:
                # If not, create a new FeatureGroup
                country_marker_groups[country] = folium.FeatureGroup(name=country)
            # Create marker for the country and add it to the respective FeatureGroup
            folium.Marker(
                location=[lat, lon],
                popup=popup_content,
                tooltip=country.capitalize()
            ).add_to(country_marker_groups[country])
            folium.Popup(popup_content, max_width=300).add_to(country_marker_groups[country])

    # Add each FeatureGroup to the map
    for country, marker_group in country_marker_groups.items():
        marker_group.add_to(folium_map)

    # Fetch geojson data for specified countries and save as geojson
    filtered_geojson_data = fetch_geojson_for_countries(countries)
    save_geojson_data(filtered_geojson_data)
    geojson_file = "filtered_countries.geojson"

    # Read population data from CSV
    population_data = pd.read_csv("population_data.csv")

    # Generate folium Choropleth layer
    folium.Choropleth(
        geo_data=geojson_file,
        name="Population",
        data=population_data,
        columns=["Country", "Population"],
        key_on="feature.properties.name",
        fill_color="YlGn",
        fill_opacity=0.4,
        line_opacity=0.2,
        legend_name="Population",
    ).add_to(folium_map)


    # Display the map
    folium.LayerControl().add_to(folium_map)
    folium_map.save("merged_map.html")


def main_menu():
    print("\nMain Menu:")
    print("1. Prerequisites and get population data (save CSV)")
    print("2. Generate Folium Markers&Choropleth Population Map for selected countries")
    print("3. Exit")


def merge_execute(cursor):
    while True:
        main_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            filename = 'population_data.csv'

            # To keep track of unique countries
            seen_countries = set()
            with open(filename, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    country = row[0]  # Assuming the country is in the first column
                    if country not in seen_countries:
                        print(country)
                        seen_countries.add(country)

            # User input
            countries = input("Enter countries (comma-separated with optional spaces): ").split(',')
            countries = [country.strip() for country in countries if country.strip()]
            print("[INFO] Selected countries: ", countries)
            years = input("Enter years (comma-separated with optional spaces): ").split(',')
            years = [year.strip() for year in years if year.strip()]

            # Get population data
            population_data = get_population_data(cursor, countries, years)
            print("[INFO] Population data fetched successfully")
            save_population_data_as_csv(population_data)

        elif choice == '2':
            plot_merged_map(population_data, countries)
            print("[INFO] Merged map saved as merged_map.html")

        elif choice == '3':
            print("Exit")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")