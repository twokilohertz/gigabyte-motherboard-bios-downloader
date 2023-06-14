# gbdl.py - GIGABYTE BIOS downloader utility

#import argparse                # For parsing command line arguments
import os                       # For filesystem access
import urllib.parse             # For parsing filenames out of URLs
import requests                 # For making requests to the website
from bs4 import BeautifulSoup   # For scraping webpages

#parser = argparse.ArgumentParser(description="Downloads BIOSes for GIGABYTE motherboards")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
gb_url = "https://www.gigabyte.com/Motherboard/X570-AORUS-ELITE-rev-10"

# Get the pages and setup Soup scraping for them
main_page = requests.get(gb_url, headers={"User-Agent": user_agent})
main_soup = BeautifulSoup(main_page.content, "html.parser")
support_page = requests.get(gb_url + "/support", headers={"User-Agent": user_agent})
support_soup = BeautifulSoup(support_page.content, "html.parser")

# Get motherboard name from page title, remove newlines, returns and whitespace
board_name = main_soup.find(class_="pageTitle").text.replace("\n", "").replace("\r", "").strip()

# Check if directory exists for motherboard, make it if it doesn't
if not os.path.isdir(board_name):
    os.mkdir(board_name)

# Get list of all rows in the BIOS downloads table
bios_downloads = support_soup.find_all(class_="div-table-row div-table-body-BIOS")

# Iterate through list
for row in bios_downloads:
    # Locate BIOS download URL
    download_url = row.find("a").get("href")
    print("Downloading: " + download_url + " ...")

    # Download the file
    download = requests.get(download_url, allow_redirects=True)

    # If successful ...
    if download.status_code == 200:
        # Open file with the filename from the URL and write the content to it
        filename = os.path.basename(urllib.parse.urlparse(download_url).path)
        target_path = (os.path.normpath(board_name + "/" + filename))

        # Write downloaded BIOS file to the file if it doesn't already exist
        if not os.path.exists(target_path):
            with open(target_path, "wb") as file:
                file.write(download.content)
        else:
            print("{} already exists, skipping...".format(target_path))
    else:
        print("Response code was not 200 OK")

print("Done!")
