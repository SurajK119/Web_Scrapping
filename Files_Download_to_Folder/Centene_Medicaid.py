# Import the required libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Collect required URL from the excel file
df = pd.read_excel("Centene_BrowsebyState.xlsx", sheet_name="Medicaid")
urls = df["Final links"]

# Iterate through all URL's
for url in urls:
    # Handle the Exception
    try:
        # Checking if any URL is NaN or having different structure
        if pd.notna(url) and isinstance(url, str) and '://' in url:  
            
            # Fetch URL
            response = requests.get(url)
            html_content = response.content

            # Parse HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract the available links
            links = soup.find_all("a")

            # Create a set to store the unique links
            main_links = set()

            # Collect all links
            for link in links:
                res = link.get("href")
                if res is not None:
                    if res.startswith("/"):
                        res = "https://" + url.split("/")[2] + res
                        if not res.endswith("redirect.html"):
                            if res.endswith(".pdf"):
                                main_links.add(res)
            print(list(main_links))
            print(len(list(main_links)))
    except Exception as e:
        print(f'Error downloading {link}: {str(e)}')