# Country Scraper

## Description
This project scrapes countries data from (https://www.scrapethissite.com/pages/simple/), including names, capitals, populations, and area. It illustrates web scraping, data collection, and structured dataset creation using Python and Pandas.

## Tools & Libraries
- Python 3
- requests
- BeautifulSoup4
- pandas

## Features
- Extracts country metadata (name, capital, population, area)
- Converts area and population to numeric for analysis
- Outputs structured CSV and JSON datasets

## How to run
1. Install required libraries:
   ```bash
   pip install requests beautifulsoup4 pandas lxml

2. Run the scraper:
    ```bash
    python scraper.py

3. Check the generated "data/country_data.csv" and "data/country_data.json"

## Sample Output
				
			

| Country | Capital | Population | Area |
| -------------------- | ----- | :---: | -------- |
| Andorra | Andorra la Vella | 84000 | 468.0 |

## Notes

- Only one request to scrape the data on a single page (no pagination)

- Designed for learning and portfolio purposes
