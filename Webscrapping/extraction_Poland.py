#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:19:34 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup

# %%

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

# Defining a decoding function
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

# %%

# Creating an empty list to store results
lawyer_links = []

# Looping across pages to get all lawyer links
for page in range(1, 215):
    
    # Define the root URL to scrap:
    root_url = f"https://rejestradwokatow.pl/adwokat/list/strona/{page}/sta/2"

    # Fetching/parsening
    page_response = requests.get(root_url, 
                                 headers = headers)
    page_soup     = BeautifulSoup(page_response.text, "lxml")
    time.sleep(2)
    
    for row in page_soup.findAll("tr")[1:]:
        link = row.select_one("tr > td:nth-child(8) > a").get("href")
        print(link)
        lawyer_links.append(link)

# %%

# Saving links as CSV  
links = pd.DataFrame(lawyer_links)
links.to_csv("URLs/Poland_links.csv", 
             index    = False, 
             encoding = "utf-8")

# %%

# Reading links CSV (if necessary)
lawyer_links = pd.read_csv("URLs/Poland_links.csv")["0"].tolist()

# %%

# Creating an empty list to store results
lawyers_list = []

# %%
# Setting up a counter
N = 9101

# Looping across retrieved links
for link in lawyer_links[N:10001]:

    # Current count
    print("Extracting information for lawyer number:" + str(N))

    # Fetching/parsening
    record_response = requests.get(link, headers = headers)
    record_soup     = BeautifulSoup(record_response.text, "lxml")
    time.sleep(5)

    # Retrieving information
    personal_info   = record_soup.find("div", class_ = "line_list_K")

    name            = record_soup.find("section").find("h2").text.strip()
    status          = personal_info.find("span", string = re.compile("Status:")).find_next_sibling("div").text.strip()
    registered_on   = personal_info.find("span", string = re.compile("Data wpisu w aktualnej")).find_next_sibling("div").text.strip()

    try:
        address   = personal_info.find("span", string = re.compile("Adres do korespondencji")).find_next_sibling("div").text.strip()
        address   = re.sub("\t|\n", ",", address)
        address   = re.sub("\s\s", "", address)
    except AttributeError:
        address   = "NA"
        
    try: 
        phone       = personal_info.find("span", string = re.compile("Komórkowy")).find_next_sibling("div").text.strip()
    except AttributeError:
        phone       = "NA"

    try: 
        email       = personal_info.find("span", string = re.compile("Email")).find_next_sibling("div")
        email       = email.get("data-ea") + "@" + email.get("data-eb")
    except AttributeError:
        email       = "NA"

    subpanel     = record_soup.find("div", class_ = "mb_tab_content special_one")

    try:
        office_info  = subpanel.find("div", class_ = "line_list_K").text
        office_info  = re.sub("\t|\n", ",", office_info)
        office_info  = re.sub("\s\s", "", office_info)
    except AttributeError:
        office_info  = "NA"

    try:
        proffesional_phone = re.search("(?<=Komórkowy:).+?(?=,)", office_info).group().strip()
    except AttributeError:
        proffesional_phone = "NA"

    try:
        proffesional_email = subpanel.find("div", class_ = "line_list_K").find("a", class_ = "__cf_email__").get("data-cfemail")
        proffesional_email = cfDecodeEmail(proffesional_email)
    except AttributeError:
        proffesional_email = "NA"

    try:
        specs  = subpanel.select_one("div > div.line_list_A > div").text.strip()
    except AttributeError:
        specs  = "NA"

    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "status"             : status,
        "reg_date"           : registered_on,
        "address"            : address,
        "phone"              : phone,
        "email"              : email,
        "office_info"        : office_info,
        "proffesional_phone" : proffesional_phone,
        "proffesional_email" : proffesional_email,
        "specializations"    : specs,
        "URL"                : link
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Upddating counter
    N = N + 1

#%%   
     
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Poland_batch1.csv", index = False, encoding = "utf-8") 

