import requests
import pycountry


def convert_country_name_to_code(country_name):
    try:
        country_obj = pycountry.countries.get(name=country_name)
        if country_obj:
            return country_obj.alpha_3.lower()
        else:
            return country_name.lower()
    except LookupError:
        print("Invalid country name")
        return None
    

def get_country_population(country, year):
    # Convert country name to code if needed
    country_code = country.lower() if len(country) <= 3 else convert_country_name_to_code(country)

    # Define parameters for the API request
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?date={year}"
    params = {
        "format": "json",
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract population data from the response
        if data and len(data) > 1 and isinstance(data[1], list) and data[1] and isinstance(data[1][0], dict) and "value" in data[1][0]:
            population = data[1][0]["value"]
            return population
        else:
            print(f"[WARNING] Population data not found or invalid for {country} in {year}.")
            return None
    else:
        print("[ERROR] Failed to retrieve data from World Bank API")
        return None