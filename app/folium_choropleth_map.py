import csv
import folium
import pandas as pd
import requests
import json


def fetch_geojson_for_countries(countries):
    # Fetch GeoJSON data for all countries from Natural Earth
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse GeoJSON data
        geojson_data = response.json()

        # Filter GeoJSON data for the specified countries
        filtered_geojson_data = {}
        for feature in geojson_data["features"]:
            country_name = feature["properties"].get("name")
            if country_name and country_name.strip().lower() in [country.strip().lower() for country in countries]:
                filtered_geojson_data[country_name.strip()] = feature

        #print("[INFO] GeoJSON data fetched successfully.")  # Debug print
        return filtered_geojson_data
    else:
        print("[ERROR] Failed to fetch GeoJSON data for all countries.")
        return None


def save_geojson_data(filtered_geojson_data):
    output_file = "filtered_countries.geojson"  # Specify the output file path
    # Create a new GeoJSON object
    output_geojson = {
        "type": "FeatureCollection",
        "features": list(filtered_geojson_data.values())
    }

    with open(output_file, "w") as f:
        json.dump(output_geojson, f, indent=4)
    print(f"[INFO] Saved GeoJSON data to {output_file}")


def create_choropleth_map():
    geojson_file = "filtered_countries.geojson"

    # Read population data from CSV
    population_data = pd.read_csv("population_data.csv")

    # Create a map centered at (0, 0)
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Add choropleth layer
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
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save("choropleth_map.html")

    print("[INFO] Choropleth map saved as choropleth_map.html")


def main_menu():
    print("\nMain Menu:")
    print("1. Prerequisites, countries selection")
    print("2. Fetch geojson, save it and create choropleth map")
    print("3. Exit")


def choropleth_execute():
    while True:
        main_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            filename = 'population_data.csv'

            seen_countries = set()  # To keep track of unique countries

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

        elif choice == '2':
            # Fetch GeoJSON data for the countries
            filtered_geojson_data = fetch_geojson_for_countries(countries)

            if filtered_geojson_data:
                print("[INFO] Geojson data for selected countries fetched properly")
                save_geojson_data(filtered_geojson_data)
                create_choropleth_map()

        elif choice == '3':
            print("Exit")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")