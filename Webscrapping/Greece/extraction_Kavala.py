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
from bs4 import BeautifulSoup
from selenium import webdriver

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path = '/Users/carlostorunopaniagua/Documents/GitHub/chromedriver',
                          options         = options)

#%%

# Creating an empty list to store results
lawyers_list = []

# List with the suffix of the URLs that we want to scrap
extension = ["2008-08-09-09-02-53",
             "2008-08-09-09-04-48",
             "2008-08-09-09-08-47",
             "2008-08-09-09-12-46",
             "2008-08-09-09-16-16",
             "2008-08-09-09-18-09",
             "2008-08-18-12-03-06"]

for ext in extension:
    root_url = f"https://www.dskavalas.gr/portal/index.php/2008-07-28-09-47-29/{ext}"

    # Getting website in the driver
    driver.get(root_url)

    # Fetching/Parsening
    content = driver.page_source
    soup    = BeautifulSoup(content)

    for row in soup.find("tbody").findAll("tr"):
        try:
            name = row.find("strong").text.strip()
        except AttributeError:
            name = "NA"

        try:
            email = row.find("a").find("a").get("href")
        except AttributeError:
            try:
                email = row.find("a").get("href")
            except AttributeError:
                email = "NA"

        info = row.text
        try:
            address = re.search("(?<=\d{3}\)).+(?=Τηλ)", info).group().strip()
        except AttributeError:
            address = ""

        try:
            phones  = re.search("(?<=Τηλ\.:).+(?=E-mail)", info).group().strip()
        except AttributeError:
            phones = ""

        try:
            languages = re.search("(?<=μετάφρασης:).+$", info).group().strip()
        except AttributeError:
            languages = "NA"

        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phones"             : phones,
            "email"              : email,
            "languages"          : languages
            }  
        
        # Appending to main list
        lawyers_list.append(lawyer)

    #%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Kavala_lawyers.csv", index = False, encoding = "utf-8")  
