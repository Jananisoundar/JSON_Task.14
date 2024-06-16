import requests
from collections import defaultdict

# Base URL of the Open Brewery DB API
BASE_URL = "https://api.openbrewerydb.org/breweries"

# States of interest
states = ["Alaska", "Maine", "New York"]

# Function to get breweries by state
def get_breweries_by_state(state):
    breweries = []
    page = 1
    while True:
        response = requests.get(BASE_URL, params={'by_state': state, 'per_page': 50, 'page': page})
        if response.status_code != 200 or not response.json():
            break
        breweries.extend(response.json())
        page += 1
    return breweries

# Initialize data structures to hold results
breweries_by_state = {state: [] for state in states}
brewery_counts_by_state = {state: 0 for state in states}
brewery_types_by_city = {state: defaultdict(lambda: defaultdict(int)) for state in states}
breweries_with_websites = {state: [] for state in states}

# Fetch and process data for each state
for state in states:
    breweries = get_breweries_by_state(state)
    breweries_by_state[state] = [brewery['name'] for brewery in breweries]
    brewery_counts_by_state[state] = len(breweries)
    for brewery in breweries:
        city = brewery['city']
        brewery_type = brewery['brewery_type']
        brewery_types_by_city[state][city][brewery_type] += 1
        if brewery['website_url']:
            breweries_with_websites[state].append(brewery['name'])

# 1. List the names of all breweries in Alaska, Maine, and New York
print("Names of breweries by state:")
for state in states:
    print(f"{state}:")
    for name in breweries_by_state[state]:
        print(f"  - {name}")

# 2. Count of breweries in each state
print("\nCount of breweries by state:")
for state, count in brewery_counts_by_state.items():
    print(f"{state}: {count}")

# 3. Count the number of types of breweries present in individual cities
print("\nNumber of types of breweries by city:")
for state, cities in brewery_types_by_city.items():
    print(f"{state}:")
    for city, types in cities.items():
        print(f"  {city}:")
        type_count = len(types)
        print(f"    Number of types of breweries: {type_count}")
        for brewery_type, count in types.items():
            print(f"      {brewery_type}: {count}")

# 4. Count and list of breweries with websites
print("\nBreweries with websites by state:")
for state, breweries in breweries_with_websites.items():
    print(f"{state}: {len(breweries)}")
    for brewery in breweries:
        print(f"  - {brewery}")
