import requests # For making HTTP requests to the API
import pandas as pd # For handling data in table form and exporting to CSV
import os # Needed to access environment variables (like API key) securely

# API endpoint URL for municipal libraries data
url = "https://api.golemio.cz/v2/municipallibraries"

# Use environment variable for API key to avoid hardcoding it in the script
api_key = os.getenv("GOLEMIO_API_KEY")
headers = {"x-access-token": api_key} if api_key else {}

# Send a GET request to the API with the authorization header
response = requests.get(url, headers=headers)
# print(response.json()) - see what keys exist at the top level here, or see in API documentation

# Extract the list of library entries "features" key
data = response.json()["features"]

# An empty list to collect the extracted library data
extracted = []

# Loop through each library entry
for item in data:
    props = item.get("properties", {})  # Extract the "properties" dictionary with library details (default to empty if missing)
    coords = item.get("geometry", {}).get("coordinates", [None, None]) # Extract coordinates from the "geometry" dictionary; default to [None, None] if missing

    # Create empty opening hours for each day of the week
    open_hours = {
        "Monday": "",
        "Tuesday": "",
        "Wednesday": "",
        "Thursday": "",
        "Friday": "",
        "Saturday": "",
        "Sunday": ""
    }

    # Fill in available default hours per day
    for entry in props.get("opening_hours", []): # Loop through each opening hours entry in the library's data
        if entry.get("is_default"): # Made decision to only look at entries marked as default opening hours
            day = entry.get("day_of_week")
            opens = entry.get("opens")
            closes = entry.get("closes")
            open_hours[day] = f"{opens}-{closes}" # format

    # Add extracted data to the list as a dictionary
    extracted.append({
        "ID_kniznice": props.get("id"),
        "Nazov_kniznice": props.get("name"),
        "Ulica": props.get("address", {}).get("street_address"),
        "PSC": props.get("address", {}).get("postal_code"),
        "Mesto": props.get("address", {}).get("address_locality"),
        "District": props.get("district"),
        "Krajina": props.get("address", {}).get("address_country"),
        "Zemepisna_sirka": coords[1],  # Latitude
        "Zemepisna_dlzka": coords[0],  # Longitude
        "Cas_otvorenia_Monday": open_hours["Monday"],
        "Cas_otvorenia_Tuesday": open_hours["Tuesday"],
        "Cas_otvorenia_Wednesday": open_hours["Wednesday"],
        "Cas_otvorenia_Thursday": open_hours["Thursday"],
        "Cas_otvorenia_Friday": open_hours["Friday"],
        "Cas_otvorenia_Saturday": open_hours["Saturday"],
        "Cas_otvorenia_Sunday": open_hours["Sunday"],
    })

# Create a DataFrame from the extracted data
df = pd.DataFrame(extracted)

# Export the DataFrame to a CSV file
df.to_csv("libraries.csv", index=False)
