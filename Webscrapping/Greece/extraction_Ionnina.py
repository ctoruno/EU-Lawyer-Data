#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 2022

@author: carlostorunopaniagua
"""

# Libraries needed
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

#%%

# Defining an empty list to store extracted links
link_list = []

# Looping across pagination
for page in range(1,23):

    print("Curently extracting links from page: " + str(page))
    
    # Fetching/Paresening
    root_url = f"https://www.dsioan.gr/members/home/page:{page}"
    response = requests.get(root_url)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(3)
        
    # Looping across lawyers
    for row in soup.findAll("div", class_ = "member"):
        link = row.find("a", class_ = "overlay_link").get("href")
        link = "https://www.dsioan.gr" + link
        link_list.append(link)

#%%

# Saving links as CSV  
links = pd.DataFrame(link_list).drop_duplicates()
links.to_csv("IONNINA_links.csv", index = False, encoding = "utf-8")

#%%

# Setting up a counter
N = 0

# Creating an empty list to store results
lawyers_list = []

# Looping across links:
for plink in link_list:

    print("Currently on individual number: " + str(N))
    
    #Fetching/Parsening
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(3)

    # Retrieving info
    name = soup.find("h1").text.strip()

    try:
        phone1 = soup.find("p", class_ = "member_icon member_phone").text.strip()
        phone1 = re.search("(?<=Τηλέφωνο:\s).+", phone1).group()
    except AttributeError:
        phone1 = "NA"

    try:
        phone2 = soup.find("p", class_ = "member_icon member_mobile").text.strip()
        phone2 = re.search("(?<=Κινητό:\s).+", phone2).group()
    except AttributeError:
        phone2 = "NA"
    
    try:
        email = soup.find("p", class_ = "member_icon member_email").text.strip()
        email = re.search("(?<=Email:\s).+", email).group()
    except AttributeError:
        email = "NA"
    
    try:
        address = soup.find("p", class_ = "member_icon member_address").text.strip()
        address = re.search("(?<=Διεύθυνση:\s).+", address).group()
    except AttributeError:
        address = "NA"
    
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "address"            : address,
        "phone1"             : phone1,
        "phone2"             : phone2,     
        "email"              : email,
        "URL"                : plink
        }  
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Updating counter
    N = N + 1

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("IONNINA_lawyers.csv", index = False, encoding = "utf-8")  
