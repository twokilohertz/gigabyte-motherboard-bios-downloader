# gbdl.py - GIGABYTE BIOS downloader utility

#import argparse # For parsing command line arguments
import os # For filesystem access
import urllib.parse # For parsing filenames out of URLs
import requests # For making requests to the website
from bs4 import BeautifulSoup # For scraping webpages

#parser = argparse.ArgumentParser(description="Downloads BIOSes for GIGABYTE motherboards")

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
gb_url = "https://www.gigabyte.com/Motherboard/B450M-DS3H-rev-1x"

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
        with open((os.path.normpath(board_name + "/" + filename)), "wb") as file:
            file.write(download.content)

print("Done!")