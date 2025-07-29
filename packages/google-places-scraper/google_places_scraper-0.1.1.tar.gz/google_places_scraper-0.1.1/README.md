# Google Places Scraper

A Python wrapper and CLI tool to scrape nearby places using the Google Places API. Useful for lead generation, local business discovery, and location data gathering.

---

## ✨ Features

- 🔍 Search places by location, radius, and type (e.g., schools, hospitals)
- 📞 Fetch detailed info: address, phone, website
- 📤 Export results as CSV, JSON, or YAML
- 💰 Log request stats and estimated cost per Google API pricing
- 🖥️ Use via Python or command-line (CLI)

---

## 📦 Installation

From PyPI:
```bash
pip install google-places-scraper
```

From local build:
```bash
pip install dist/google_places_scraper-0.1.0-py3-none-any.whl
```

For development (editable mode):

```bash
pip install -e .
```

---
## 🐍 Python Usage

You can use it directly in your Python scripts:

```
from google_places_scraper import GooglePlacesScraper

scraper = GooglePlacesScraper(api_key="YOUR_GOOGLE_API_KEY")
scraper.run(
    user_location_input="Karachi, Pakistan",
    radius=3000,
    type_="school",
    export_format="csv",  # Options: csv, json, yaml
    max_results=50
)
```
---
## 🚀 CLI Usage
After installation, run the CLI:

```bash
google-places-scraper
```

You’ll be prompted to enter:

Enter your Google Places API Key: AIzaxxxxx
Enter location name or 'latitude,longitude': Karachi
Enter radius in meters (default 5000): 3000
Export format (csv/json/yaml) [default=csv]: csv
Enter type of place (default=school): school
Max number of results (leave blank for no limit): 10

---

## 📄 Output
The tool generates one of the following files based on your export format:

leads.csv

leads.json

leads.yaml

Containing the following fields:

name

formatted_address

formatted_phone_number

website

Example (CSV):

name,formatted_address,formatted_phone_number,website
"ABC School","Main Street, Karachi","021-1234567","http://abcschool.edu.pk"

---
## 🛠 Development
Build the package:

rm -rf dist build *.egg-info
python -m build

or

make install

then

twine upload dist/*

Reinstall after changes:

pip install --force-reinstall dist/google_places_scraper-0.1.0-py3-none-any.whl

---