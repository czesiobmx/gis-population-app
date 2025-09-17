import pycountry
import sys
from population_get import get_country_population
from alpha2_contry_codes_lib import continent_codes
import time


def fetch_countries(continent_name):
    # Fetch country codes based on the continent name
    continent_codes_list = continent_codes.get(continent_name, [])

    # Fetch country objects using pycountry
    countries = [pycountry.countries.get(alpha_2=code) for code in continent_codes_list]

    # Remove None values (countries not found in pycountry)
    countries = [country for country in countries if country is not None]

    return countries


def show_countries(countries):
    # Display the list of countries
    print("Selected continent countries:")
    print("+------------------------------------------+-------------+")
    print("| Country Name                             | Alpha-3 Code|")
    print("+------------------------------------------+-------------+")
    for country in countries:
        # Replace specific characters
        name_replaced = country.name.replace("ç", "c").replace("é", "e").replace("ü", "u").replace("ô", "o")
        print(f"| {name_replaced:<40} | {country.alpha_3:<11} |")
    print("+------------------------------------------+-------------+")


def fetch_population(countries, year):
    # Define a variable to keep track of the number of API requests
    api_request_count = 0
    country_data = {}

    for country in countries:
        # wait before sending the request (throttling protection)
        time.sleep(1)

        start = time.perf_counter()
        population = get_country_population(country.alpha_2, year)
        elapsed = time.perf_counter() - start       

        if population:
            country_data[country.name] = population
            api_request_count += 1
            # Display the loading message with live updates
            sys.stdout.write(f"\rFetching population data (API requests: {api_request_count})... Request for {country.name} ({year}) took {elapsed:0.2f} seconds.")
            sys.stdout.flush()

    print("Population data:")
    print("+-----------------------------------------+----------------+")
    print("| Country Name                            | Population     |")
    print("+-----------------------------------------+----------------+")
    for country, population in country_data.items():
        name_replaced = country.replace("ç", "c").replace("é", "e").replace("ü", "u").replace("ô", "o")
        print(f"| {name_replaced:<39} | {population:>14,} |")
    print("+-----------------------------------------+----------------+")

    return country_data, year