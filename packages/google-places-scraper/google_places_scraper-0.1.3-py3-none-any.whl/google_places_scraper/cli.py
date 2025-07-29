from google_places_scraper import GooglePlacesScraper

def main():
    api_key = input("Enter your Google Places API Key: ").strip()
    location_input = input("Enter location name or 'latitude,longitude': ").strip()
    radius = int(input("Enter radius in meters (default 5000): ") or 5000)
    format_ = input("Export format (csv/json/yaml) [default=csv]: ").strip().lower() or "csv"
    type_ = input("Enter type of place (default=school): ").strip() or "school"
    max_results_input = input("Max number of results (leave blank for no limit): ").strip()
    max_results = int(max_results_input) if max_results_input.isdigit() else None

    scraper = GooglePlacesScraper(api_key)
    scraper.run(location_input, radius, export_format=format_, type_=type_, max_results=max_results)

if __name__ == "__main__":
    main()
