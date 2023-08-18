#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 2022

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
root_url = "https://www.dskalamatas.gr/o-syllogos/meli"
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")

for row in (soup.find("tbody").findAll("tr")):
    name = row.select_one("tr > td:nth-child(1)").text
    name = re.sub("\n", " ", name).strip()

    address = row.select_one("tr > td:nth-child(2)").text
    address = re.sub("\n", " ", address).strip()

    email = row.select_one("tr > td:nth-child(3)").text
    email = re.sub("\n", " ", email).strip()

    phones = row.select_one("tr > td:nth-child(4)").text.strip()
    phones = re.sub("\n", "<>", phones)

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
master_data.to_csv("Kalamata_lawyers.csv", index = False, encoding = "utf-8") 



    
