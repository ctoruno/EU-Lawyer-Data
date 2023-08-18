#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 2022

@author: carlostorunopaniagua
"""

# Libraries needed
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

#%%

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

#%%

# List of websites where the links are located
URLs     = ["https://www.dsxanthi.gr/E82C2064.el.aspx?splitter_children_offset=0",
            "https://www.dsxanthi.gr/E82C2064.el.aspx?splitter_children_offset=20",]

# Creating an empty list to store the results
link_list = []

# Extracting the links
for URL in URLs:

    # Fetching/Paresening
    response = requests.get(URL, headers = headers)
    soup     = BeautifulSoup(response.text, "lxml")

    for block in soup.findAll("div", class_ = "tile"):
        link = block.find("a").get("href")
        link_list.append(link)

#%%

# Creating an empty list to store results
lawyers_links = []

for extension in link_list:

    # Defining root URL
    root_url = f"https://www.dsxanthi.gr/{extension}"

    # Fetching/Parsening
    response = requests.get(root_url, headers = headers)
    soup     = BeautifulSoup(response.text, "lxml")

    # For a reason I can't understand, one page has a different structure:
    if root_url == "https://www.dsxanthi.gr/1D6B0A99.el.aspx":
        continue

    # Locating rows with lawyers links
    table = soup.find("div", {"id": "ChildrenArea"}).findAll("tr")

    # If page has information, then
    if len(table) > 0:

        # Counting rows
        N = 1

        for row in table:
            print(N)

            # For the first 20 rows we extract the links
            if N < 21:
                lawyer_link = row.find("div", class_ = "eqcol").find("a", class_ = "link").get("href")
                lawyers_links.append(lawyer_link)

                # We update the row counter
                N = N+1
            
            # For the next ones, we pass to the next page
            if N == 21:

                # URL for new page
                root_url = root_url + "?splitter_children_offset=20"

                # Fetching/Parsening
                response = requests.get(root_url, headers = headers)
                soup     = BeautifulSoup(response.text, "lxml")

                # Extarcting info
                lawyer_link = row.find("div", class_ = "eqcol").find("a", class_ = "link").get("href")
                lawyers_links.append(lawyer_link)

                # We update the row counter
                N = N+1

#%%    

# Extracting the info from the page that has a different structure

# First 20 tiles:

# Defining root URL
root_url = f"https://www.dsxanthi.gr/1D6B0A99.el.aspx"

# Fetching/Parsening
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")

# Counting rows
N = 1

# Looping across tiles
for tile in soup.findAll("div", class_ = "tile"):

    print(N)

    # For the first 20 tiles, we extract the info
    if N < 21:
        lawyer_link = tile.find("a").get("href")
        lawyers_links.append(lawyer_link)
        N = N+1

# Last 20 tiles:

# Re-defining root URL
root_url = root_url + "?splitter_children_offset=20"
        
# Fetching/Parsening
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")

# Looping across tiles
for tile in soup.findAll("div", class_ = "tile"):

    print(N)

    # For the first 20 tiles, we extract the info
    lawyer_link = tile.find("a").get("href")
    lawyers_links.append(lawyer_link)
    N = N+1

#%%

# Defining a decoding function
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

#%%

# Setting up counter
N = 0

# Creating an empty list to store results
lawyers_list = []

for link in lawyers_links:

    # Defining root URL
    root_url = f"https://www.dsxanthi.gr/{link}"

    # Fetching/Parsening
    response = requests.get(root_url, headers = headers)
    soup     = BeautifulSoup(response.text, "lxml")
    print(N)
    time.sleep(2)

    # Extracting info
    info_raw   = soup.find("div", class_ = "clearfix")
    info_block = info_raw.text

    name = soup.find("h1").text.strip()

    try:
        address = re.search("(?<=\n).+(?=\nΤηλ)", info_block).group()
    except AttributeError:
        try:
            address = re.search("^.+(?=Τηλ)", info_block).group()
        except AttributeError:
            address = "NA"

    try:
        phone = re.search("(?<=Τηλέφωνα : ).+(?=\n)", info_block).group().strip()
    except AttributeError:
        phone = "NA"

    try:
        email = info_raw.find("a").get("href")
        email = re.search("(?<=#).+", email).group()
        email = cfDecodeEmail(email)
    except AttributeError:
        email = "NA"

    if email == "NA":
        try:
            email = info_raw.find("a").find("span").get("data-cfemail")
            email = cfDecodeEmail(email)
        except AttributeError:
            email = "NA"

    if email == "NA":
        try:
            email = info_raw.find("a").get("data-cfemail")
            email = cfDecodeEmail(email)
        except (TypeError, AttributeError) as error:
            email = "NA"
    
    try:
        conditional = info_raw.find("a").get("href")
    except AttributeError:
        conditional = False

    if email == "NA" and conditional == True:
        try:
            email = info_raw.find("a").get("href")
        except AttributeError:
            email = "NA"

    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "address"            : address,
        "phone"              : phone,
        "email"              : email,
        "URL"                : link
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)

    # Updating counter
    N = N+1

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Xanthi_lawyers.csv", index = False, encoding = "utf-8") 
