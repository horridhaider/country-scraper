import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configuring Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

final_data = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}

# Function to send request and fetch data from webpage
def scrape_pages(url):    
    logging.info("Sending request to the website...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    logging.info("Request Successful!")
    return response

# Function to parse the html and obtain necessary data
def extract_data(response):
    soup = BeautifulSoup(response.content, "lxml")
    country_tags = soup.find_all("div", class_="col-md-4 country")
    logging.info(f"Found {len(country_tags)} country blocks")
    country_data = []

    for country in country_tags:
        try:
            name = country.find("h3", class_="country-name").text.strip()
            capital = country.find("span", class_="country-capital").text.strip()
            population = country.find("span", class_="country-population").text.strip()
            area = country.find("span", class_="country-area").text.strip()
        except AttributeError as e:         # This will just skip one book, instead of breaking whole code
            logging.warning(f"Skipping one country block because of missing data: {e}")
            continue

        # Appending data to our main global list
        country_data.append({
            "Country": name,
            "Capital": capital,
            "Population": population,
            "Area": area        # in square kilometers
        })
    return country_data

# This saves data into CSV and JSON using Pandas
def save_data(final_data):
    df = pd.DataFrame(final_data)   # makes dataframe in pandas
    logging.info("Converting numeric columns...")
        # This changes the format of Population and Area to numeric so that data analysis can be easy
    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
    df["Area"] = pd.to_numeric(df["Area"], errors="coerce")
    logging.info("Removing Duplicates...")
    df = df.drop_duplicates()       # this removes the duplicates if found
    
    logging.info("Saving data into .csv and .json...")
    df.to_csv("country_data.csv", index=False, encoding="utf-8-sig")
    df.to_json("country_data.json", orient="records", force_ascii=False, indent=4) # the presentable formatting of json
    logging.info("Save Successful!")
    logging.info("Data has been successfully saved into .csv and .json !")
    print("Displaying a Preview...")
    print(df.head())    # previews some starting blocks of data


try:
    # this safely sends request to the site...
    response = scrape_pages("https://www.scrapethissite.com/pages/simple/")     # stores response in a variable
    data = extract_data(response)       # extracts data by parsing html in BeautifulSoup and stores in a variable
    final_data.extend(data)     # Pandas uses that extracted data and saves that into CSV and JSON after cleaning & formatting

except requests.exceptions.ConnectionError:
    logging.error("No Internet - Unable to Connect to the Site.")
except requests.exceptions.Timeout:
    logging.error("Request Timed Out.")
except requests.HTTPError:
    logging.error("HTTP error occurred.")
except AttributeError:
    logging.error("Request Unsuccessful.")
except Exception as e:
    logging.exception(f"Unexpected error: {e}")

finally:    # whatever goes wrong in code, this finally block would save the data in this 'finally' block
    if final_data:
        save_data(final_data=final_data)