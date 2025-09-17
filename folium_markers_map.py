import csv
import matplotlib.pyplot as plt
import folium
from matplotlib.ticker import FuncFormatter
from geopy.geocoders import Nominatim
import time


# Function to get population data for selected countries and years
def get_population_data(cursor, countries, years):
    population_data = {}

    for country in countries:
        population_data[country] = {}
        for year in years:
            query = "SELECT Population FROM countries_population WHERE Country = %s AND Year = %s"
            cursor.execute(query, (country.strip(), year.strip()))
            result = cursor.fetchone()
            if result:
                population_data[country][year] = result[0]
            else:
                population_data[country][year] = None
    print("[INFO] Population data dictionary: ", population_data)
    return population_data


def save_population_data_as_csv(population_data):
    output_file = "population_data.csv"
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Country', 'Population'])  # Write header row
        for country, data in population_data.items():
            for year, population in data.items():
                writer.writerow([country, population])
    print("[INFO] Population data saved as", output_file)


# Plot population data
def plot_population_data(population_data):
    for country, data in population_data.items():
        plt.plot(list(data.keys()), list(data.values()), marker='o', label=country)

    plt.xlabel('Year')
    plt.ylabel('Population (Millions)')
    plt.title('Population of Selected Countries Over Time')
    plt.grid(True)

    # Move legend outside to the right
    plt.legend(
        loc="center left",          # put legend to the left of the anchor box
        bbox_to_anchor=(1.05, 0.5)  # shift it outside the plot area
    )

    # Format y-axis labels as millions
    formatter = FuncFormatter(lambda x, _: '{:,.0f}'.format(x / 1e6))
    plt.gca().yaxis.set_major_formatter(formatter)
    return plt


def get_country_coordinates(country, geolocator):
    # Get country capital based on country name
    location = geolocator.geocode(country, exactly_one=True)

    # Respect Nominatim's usage policy (1 request per second)
    time.sleep(1)

    # Check if location is found
    if location:
        # Return latitude and longitude as a list
        return [location.latitude, location.longitude]
    else:
        # If location is not found, return [0, 0]
        return [0, 0]  # Default to [0, 0] if coordinates are not found


def plot_folium_map_with_markers(population_data):
    # Initialize geolocator once
    geolocator = Nominatim(user_agent="country_coordinates")

    # Initialize a map centered at a specific location
    folium_map = folium.Map(location=[0, 0], zoom_start=2)

    # Add markers for countries with available coordinates
    for country, data in population_data.items():
        lat, lon = get_country_coordinates(country, geolocator)
        if lat is not None and lon is not None:
            popup_content = f"<b>{country}</b><br>"
            for year, population in data.items():
                # Format population with commas as thousands separator
                formatted_population = "{:,}".format(population)
                popup_content += f"<div>{year} - {formatted_population}</div>"
            marker = folium.Marker(location=[lat, lon], popup=popup_content, tooltip=country.capitalize())
            marker.add_to(folium_map)
            # Adjust marker width based on content
            folium.Popup(popup_content, max_width=300).add_to(marker)

    # Display the map
    folium.LayerControl().add_to(folium_map)
    folium_map.save("markers_map.html")


def main_menu():
    print("\nMain Menu:")
    print("1. Prerequisites and get population data (save CSV)")
    print("2. Create a graph and markers map")
    print("3. Exit")


def markers_execute(cursor):
    while True:
        main_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            # User input
            countries = input("Enter countries (comma-separated with optional spaces): ").split(',')
            countries = [country.strip() for country in countries if country.strip()]

            years = input("Enter years (comma-separated with optional spaces): ").split(',')
            years = [year.strip() for year in years if year.strip()]

            # Get population data
            population_data = get_population_data(cursor, countries, years)
            print("[INFO] Population data fetched successfully")
            save_population_data_as_csv(population_data)

        elif choice == '2':

            # Option to save graph to PNG
            save_graph = input("Do you want to save the graph to a PNG file? (yes/no): ").lower()
            if save_graph == "yes" or save_graph == "y":
                plot_population_data(population_data)
                file_name = input("Enter the file name: ")
                plt.savefig(file_name + ".png", bbox_inches='tight')
                print(f"[INFO] Graph saved as {file_name}.png")

            # Option to generate folium map with markers
            folium_with_markers = input("Do you want to generate a folium map? (yes/no): ").lower()
            if folium_with_markers == "yes" or folium_with_markers == "y":
                plot_folium_map_with_markers(population_data)
                print("[INFO] Markers map saved as markers_map.html")

        elif choice == '3':
            print("Exit")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")