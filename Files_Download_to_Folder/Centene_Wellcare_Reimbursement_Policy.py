# Import the required libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Path of excel or CSV file
file_path = r"C:\Users\Suraj\Desktop\Centene_BrowsebyState.xlsx"

# Collect required URL from the excel file
df = pd.read_excel(file_path, sheet_name="Wellcare")
urls = df["Reimbursement Policy"]

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
            visited_urls = set()

            # Collect all links
            for link in links:
                res = link.get("href")
                if res is not None and res.startswith("/"):
                    res = "https://" + url.split("/")[2] + res
                    if "PDFs" in res and not res.endswith(".ashx"):
                        res = res.split("?")[0]

                    if "PDFs" in res and res.endswith(".ashx"):
                        res = res.replace(".ashx", ".pdf")
                        visited_urls.add(res)

            # Create directory to store the downloaded files
            folder_name = r"Centene_Wellcare_Reimbursement Policy//" + url.split("/")[-4]

            # Iterate through all Pdf files to download and store
            for link in list(visited_urls):
                try:
                    response = requests.get(link)
                    if response.status_code == 200:

                        if not os.path.exists(folder_name):
                            os.makedirs(folder_name)

                        with open(os.path.join(folder_name, link.split('/')[-1]), "wb") as f:
                            f.write(response.content)        
                        print(f'Successfully downloaded') 
                except Exception as e:
                    print(f'Error downloading {link}: {str(e)}')
                
    except Exception as e:
        print(f'Error accessing URL {url}: {str(e)}')