import requests
class CountryData:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(f"Failed to fetch data from URL: {self.url}")

    def display_country_info(self):
        if not self.data:
            print("No data available. Please fetch the data first.")
            return

        for country in self.data:
            name = country.get('name', {}).get('common', 'N/A')
            currencies = country.get('currencies', {})
            currency_info = ', '.join([f"{cur} ({details.get('name', 'N/A')} - {details.get('symbol', 'N/A')})"
                                       for cur, details in currencies.items()])
            print(f"Country: {name}, Currencies: {currency_info}")

    def display_countries_with_currency(self, currency_name):
        if not self.data:
            print("No data available. Please fetch the data first.")
            return

        countries = [country.get('name', {}).get('common', 'N/A')
                     for country in self.data
                     if any(details.get('name', '').lower() == currency_name.lower()
                            for details in country.get('currencies', {}).values())]
        print(f"Countries using {currency_name}: {', '.join(countries)}")


if __name__ == "__main__":
    country_data = CountryData("https://restcountries.com/v3.1/all")

    country_data.fetch_data()

    print("Countries, Currencies, and Currency Symbols:")
    country_data.display_country_info()

    print("\nCountries using DOLLAR as currency:")
    country_data.display_countries_with_currency("Dollar")

    print("\nCountries using EURO as currency:")
    country_data.display_countries_with_currency("Euro")


