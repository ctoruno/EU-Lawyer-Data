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
for page in range(1,5):

    print("Curently extracting links from page: " + str(page))
    
    # Fetching/Paresening
    root_url = f"https://www.dsdr.gr/members/page/{page}/"
    response = requests.get(root_url)
    soup     = BeautifulSoup(response.text, "lxml")
        
    # Looping across lawyers
    for row in soup.find("tbody").findAll("tr"):
        for person in row.findAll("td"):
            link = person.find("a", href = True)["href"]
            # print("<<<<<<<<<<<<<<NEW>>>>>>>>>>>>>")
            # print(link)
            link_list.append(link)

#%%

# Saving links as CSV  
links = pd.DataFrame(link_list).drop_duplicates()
links.to_csv("DRAMA_links.csv", index = False, encoding = "utf-8")

#%%

# Setting up a counter
N = 0

# Creating an empty list to store results
lawyers_list = []

# Looping across links:
for item in link_list:
    
    print("Currently on element " + str(N) + " of 185")
    
    #Fetching/Parsening
    plink    = item
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(3)
    
    # Retrieving info
    name = soup.find("h3", itemprop = "name").text.strip()

    status = soup.find("div", itemprop = "jobTitle").text.strip()
        
    try: 
        address = soup.find("div", itemprop = "description").text.strip()
        address = re.sub("\n", " ", address)
    except AttributeError:
        address = "NA"
    
    try: 
        phone  = phone = soup.find("div", itemprop = "text").text.strip()
        phone  = re.sub("\n", "<>", phone)
    except AttributeError:
        phone  = "NA"
    
    try: 
        email      = soup.find("a", string = "email", href = True).get("href")
        email      = re.search("(?<=mailto:).+", email).group()
    except AttributeError:
        email      = "NA"
        
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "status"             : status,
        "address"            : address,
        "phone"              : phone,
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
master_data.to_csv("DRAMA_lawyers.csv", index = False, encoding = "utf-8")  
