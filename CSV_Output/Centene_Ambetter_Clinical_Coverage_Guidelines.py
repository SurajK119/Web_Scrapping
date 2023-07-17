# Import the required libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import csv
from datetime import date

# Define a dictionary for states
di = {
    "www.ambetterofalabama.com" : "Alabama",
     "ambetter.azcompletehealth.com" : "Arizona",
     "ambetter.arhealthwellness.com" : "Arkansas",
     "www.healthnet.com": "NA",
      "ambetter.sunshinehealth.com" : "NA",
      "ambetter.pshpgeorgia.com" : "Georgia",
      "www.ambetterofillinois.com" : "Illinois",
      "ambetter.mhsindiana.com" : "Indiana",
      "ambetter.sunflowerhealthplan.com" : "NA",
      "ambetter.wellcareky.com" : "NA",
      "ambetter.louisianahealthconnect.com" : "Louisiana",
      "www.ambettermeridian.com" : "NA",
      "ambetter.magnoliahealthplan.com" : "NA",
      "ambetter.homestatehealth.com" : "NA",
      "ambetter.nebraskatotalcare.com" : "Nebraska",
      "ambetter.silversummithealthplan.com" : "NA",
      "ambetter.nhhealthyfamilies.com" : "New Hampshire",
      "ambetter.wellcarenewjersey.com": "Newjersey",
      "ambetter.westernskycommunitycare.com" : "NA",
      "www.fideliscare.org" : "NA",
      "www.ambetterofnorthcarolina.com" : "North Carolina",
      "ambetter.buckeyehealthplan.com" : "NA",
      "www.ambetterofoklahoma.com" : "Oklahoma",
      "www.healthnetoregon.com" : "Oregon",
      "ambetter.pahealthwellness.com" : "Pennsylvania",
      "ambetter.absolutetotalcare.com" : "NA",
      "www.ambetteroftennessee.com" : "Tennessee",
      "ambetter.superiorhealthplan.com" : "NA",
      "ambetter.coordinatedcarehealth.com" : "NA"
}

# Path of excel or CSV file
file_path = r"C:\Users\Suraj\Desktop\Centene_BrowsebyState.xlsx"

# Collect required URL from the excel file
df = pd.read_excel(file_path, sheet_name="Ambetter")
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
            visited_urls = set()

            # Collect all links
            for link in links:
                res = link.get("href")
                if res is not None:
                    if res.startswith("/"):
                        res = "https://" + url.split("/")[2] + res
                        if not res.endswith("redirect.html"):
                            if res.endswith(".pdf"):
                                visited_urls.add(res)
            
            for link in list(visited_urls):
                try:
                    for key in di:
                        if key == url.split("/")[2]:
                                              
                            # Create a list of dictionaries to hold the data
                            data = {'state' : [di[key]],
                                    'main_url': ["https://www.centene.com/products-and-services/browse-by-state/" + url.split("/")[-4] + ".html"],
                                    'sub_url': [url],
                                    'downloadable_link': [link],
                                    'line_of_business': ['Health Insurance Marketplace'],
                                    'type_of_service': ['NA'],
                                    'document_name': [link.split('/')[-1]],
                                    'download_date': [date.today()]
                                    }

                    # Define the CSV file path and column names
                    csv_file_path = "data.csv"
                    column_names = ['state', 'main_url', 'sub_url', 'downloadable_link', 'line_of_business', 'type_of_service', 'document_name', 'download_date']

                    # Check if file exists
                    file_exists = os.path.isfile(csv_file_path)

                    # Create and write to the CSV file
                    with open(csv_file_path, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)

                        # Write the header row if the file does not exist
                        if not file_exists:
                            writer.writerow(column_names)

                        # Write the data rows
                        for row_data in zip(*[data[column] for column in column_names]):
                            writer.writerow(row_data)

                    print(f'Data appended to CSV file: {csv_file_path}') 
                except Exception as e:
                    print(f'Error downloading {link}: {str(e)}')
                
    except Exception as e:
        print(f'Error accessing URL {url}: {str(e)}')