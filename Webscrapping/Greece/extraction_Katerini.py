#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 2022

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

# Creating an empty list to store results
lawyers_list = []

# Fetching/Paresening
root_url = "https://www.dskaterinis.gr/lawyers/"
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")

for row in soup.find("tbody").findAll("tr"):
    try:
        name    = row.select_one("tr > td:nth-child(2)").text.strip()
    except AttributeError:
        name    = "NA"

    try:
        address = row.select_one("tr > td:nth-child(3)").text.strip()
    except AttributeError:
        address = "NA"

    try:
        phones  = row.select_one("tr > td:nth-child(4)").text.strip()
    except AttributeError:
        phones  = "NA"
    
    try:
        email   = row.select_one("tr > td:nth-child(5)").text.strip()
    except AttributeError:
        email   = "NA"

    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "address"            : address,
        "phones"             : phones,
        "email"              : email,
        } 

    # Appending to main list
    lawyers_list.append(lawyer)

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Katerini_lawyers.csv", index = False, encoding = "utf-8") 

