import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: Input the target website URL (Updated Path)
url = "https://www.scrapethissite.com/pages/simple/"
print(f"Connecting to target server: {url}")
print("Sending HTTP request and waiting for response...")

# Step 2: Run the request and wait for the server to ping back
response = requests.get(url)
time.sleep(2)  # Forcing a deliberate 2-second wait to mimic heavy server data loads

if response.status_code == 200:
    print("Connection successful! Server data received. Parsing HTML markers...")

    # Step 3: Parse the active page layers
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 4: Extract live country economic data logs
    countries_data = []
    country_nodes = soup.find_all("div", class_="country")

    print(f"Extracting fields from {len(country_nodes)} country rows...")

    for node in country_nodes:
        name = node.find("h3", class_="country-name").text.strip()
        capital = node.find("span", class_="country-capital").text.strip()
        population = node.find("span", class_="country-population").text.strip()
        area = node.find("span", class_="country-area").text.strip()

        countries_data.append(
            {
                "Country": name,
                "Capital": capital,
                "Population": population,
                "Area (sq km)": area,
            }
        )

    # Step 5: Convert to Pandas matrix and save
    df = pd.DataFrame(countries_data)
    df.to_csv("global_macro_data.csv", index=False)

    print("\n--- Process Complete ---")
    print(df.head(10).to_string(index=False))  # Displays the top 10 rows
    print("\nFile saved successfully as 'global_macro_data.csv'!")
else:
    print(f"Server rejected connection. Status Code: {response.status_code}")
