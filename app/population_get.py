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
    

def get_country_population(session, country, year):
    # Convert country name to code if needed
    country_code = country.lower() if len(country) <= 3 else convert_country_name_to_code(country)

    # Define parameters for the API request
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL"
    params = {"date": year, "format": "json"}

    # Make the API request
    try:
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 1 and isinstance(data[1], list) and data[1]:
            value = data[1][0].get("value")
            if value is not None:
                return value
        print(f"[WARN] No valid population data for {country} ({year})")
    except requests.RequestException as e:
        print(f"[ERROR] {country}: {e}")
    return None