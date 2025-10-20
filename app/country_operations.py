import pycountry
import sys
from population_get import get_country_population
from alpha2_contry_codes_lib import continent_codes
import time
import requests
import concurrent.futures


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


def fetch_population(countries, year, max_workers=10):
    # Create a reusable requests session
    session = requests.Session()
    session.headers.update({"User-Agent": "PopulationFetcher/1.0"})

    country_data = {}
    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(get_country_population, session, c.alpha_2, year): c for c in countries
        }

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            country = futures[future]
            try:
                pop = future.result()
                if pop:
                    country_data[country.name] = pop
            except Exception as e:
                print(f"[ERROR] {country.name}: {e}")
            sys.stdout.write(f"\rFetched {i}/{len(countries)} countries...")
            sys.stdout.flush()

    elapsed = time.perf_counter() - start_time
    print(f"[INFO] Completed in {elapsed:.2f} seconds.\n")

    # Print table
    print("Population Data:")
    print("+-----------------------------------------+----------------+")
    print("| Country Name                            | Population     |")
    print("+-----------------------------------------+----------------+")
    for country, pop in country_data.items():
        name_fixed = country.replace("ç","c").replace("é","e").replace("ü","u").replace("ô","o")
        print(f"| {name_fixed:<39} | {pop:>14,} |")
    print("+-----------------------------------------+----------------+")

    return country_data, year