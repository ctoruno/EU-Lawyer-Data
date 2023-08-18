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
root_url = "https://dsrnet.gr/lawyers/"
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")

for row in soup.find("tbody").findAll("tr"):
    try:
        last_name  = row.select_one("tr > td:nth-child(1)").text.strip()
    except AttributeError:
        last_name  = "NA"

    try:
        first_name  = row.select_one("tr > td:nth-child(2)").text.strip()
    except AttributeError:
        first_name  = "NA"
    
    try:
        address  = row.select_one("tr > td:nth-child(3)").text.strip()
    except AttributeError:
        address  = "NA"
    
    try:
        phone  = row.select_one("tr > td:nth-child(4)").text.strip()
    except AttributeError:
        phone  = "NA"
    
    try:
        mobile  = row.select_one("tr > td:nth-child(6)").text.strip()
    except AttributeError:
        mobile  = "NA"
    
    try:
        email  = row.select_one("tr > td:nth-child(7)").text.strip()
    except AttributeError:
        email  = "NA"

    # Defining dictionary entry
    lawyer = {
        "last_name"          : last_name,
        "first_name"         : first_name,
        "address"            : address,
        "phone"              : phone,
        "mobile"             : mobile,
        "email"              : email,
        } 

    # Appending to main list
    lawyers_list.append(lawyer)

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Rhodes_lawyers.csv", index = False, encoding = "utf-8") 
