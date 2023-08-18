#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 06:41:09 2022

@author: carlostorunopaniagua
"""

# Libraries needed
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


#%%

# RETRIEVING DATA FROM CHANIA BAR ASSOCIATION

# Creating empty list to store the results
lawyers_list = []

# Looping across pages
for page in range(1, 44):
    
    print("Currently extracting info from page: " + str(page))

    # Setting pagination
    plink = f"https://dschania.org/member-cat-specialty/dikigoroi/page/{page}/"
    time.sleep(3)
    
    # Fetching/parsening
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    
    table_rows    = soup.findAll("div", class_ = "table-row table-body")
    
    # Looping across lawyers
    for row in table_rows:
        name     = row.select_one("div > div:nth-child(2) > h4").text
        category = row.select_one("div > div:nth-child(3) > h4").text
        address  = row.select_one("div > div:nth-child(4) > h4").text
        
        contact  = "<>".join([item.text for item in row.select("div > div:nth-child(5) > h4")])
        phone    = re.sub("<>", " - ", re.search("((?<=<>)|()).+((?=<>.+@)|(?=$))", contact).group())
        
        try: 
            email   = re.sub("<>", " - ", re.search("((?<=<>)|(^))(?:(?!<>).)+@.+", contact).group())
        except AttributeError:
            email   = "NA"
    
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "category"           : category
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)

    
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Greece/Greece_CHANIA.csv", index = False, encoding = "utf-8")

#%%

# RETRIEVING DATA FROM VERIA, NAOUSSA AND ALEXANDRIA BAR ASSOCIATIONs

# Defining barss URL
bars_URL = ["https://www.dsb.gr/dikigoroi/veroias.htm",
            "https://www.dsb.gr/dikigoroi/naoussas.htm",
            "https://www.dsb.gr/dikigoroi/alexandreias.htm"]

# Creating an empty list to store results
lawyers_list = []

# Looping across Bar Associations
for bar in bars_URL:
    
    # Fetching/parsening    
    response = requests.get(bar)
    soup     = BeautifulSoup(response.text, "lxml")    
    
    # Locating table
    table    = soup.find("tbody").findAll("tr") 
    
    # Looping across lawyers
    for row in table:
        name        = row.select_one("tr > td:nth-child(2)").text
        phone_firm  = row.select_one("tr > td:nth-child(3)").text
        phone_ind   = row.select_one("tr > td:nth-child(4)").text
        
        email_info  = row.select_one("tr > td:nth-child(6)").find("a", href = True)
        
        try: 
            email   = email_info["data-mlu"] + "@" + email_info["data-mld"] + "." + email_info["data-mlt"]
        except TypeError:
            email   = "NA"

        address     = row.select_one("tr > td:nth-child(7)").text
                
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone_firm"         : phone_firm,
            "phone_ind"          : phone_ind,
            "email"              : email,
            "category"           : category
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Greece/Greece_VERIA_NAOUSSA_ALEXANDRIA.csv", index = False, encoding = "utf-8")
    
#%%

# RETRIEVING DATA FROM LARISSA BAR ASSOCIATION

# Defining an empty list to store extracted links
link_list = []

# Looping across pagination
for page in range(1,14):

    print("Curently extracting links from page: " + str(page))
    
    # Fetching/Paresening
    root_url = f"https://www.dslar.gr/members/page/{page}/"
    response = requests.get(root_url)
    soup     = BeautifulSoup(response.text, "lxml")
        
    
    # Looping across lawyers
    for row in soup.find("tbody").findAll("tr"):
        for person in row.findAll("td"):
            link = person.find("a", href = True)["href"]
            # print("<<<<<<<<<<<<<<NEW>>>>>>>>>>>>>")
            # print(link)
            link_list.append(link)
    
# Saving links as CSV  
links = pd.DataFrame(link_list).drop_duplicates()
links.to_csv("Greece/Greece_LARISSA_links.csv", index = False, encoding = "utf-8")

#%%

# Setting up a counter
N = 0

# Creating an empty list to store results
lawyers_list = []

# Looping across links:
for item in link_list:
    
    print("Currently on element " + str(N) + " of 748")
    N = N + 1
    
    #Fetching/Parsening
    plink    = item
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    
    # Retrieving info
    name = soup.find("h5", itemprop = "headline").text.strip()
    
    info = soup.find("div", class_ = "flex_column av_two_third first el_before_av_one_third avia-builder-el-first")
    
    try: 
        address = info.find("strong", string = re.compile("Διεύθυνση")).find_parent().text.strip()
        address = re.search("(?<=Διεύθυνση:\s).+", address).group()
    except AttributeError:
        address = "NA"
    
    try: 
        telephones = info.findAll("strong", string = re.compile("Τηλέφωνο"))
        telephones = [re.search("(?<=Τηλέφωνο:\s).+", x.find_parent().text.strip()).group() for x in telephones]
        phone      = "<>".join(telephones) 
    except AttributeError:
        phone      = "NA"
    
    try: 
        email      = info.find("strong", string = re.compile("Email")).find_parent().text.strip()
        email      = re.search("(?<=Email:\s).+", email).group()
    except AttributeError:
        email      = "NA"
        
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "address"            : address,
        "phone"              : phone,
        "email"              : email,
        "URL"                : plink
        }  
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    time.sleep(3)

#%%
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Greece/Greece_LARISSA.csv", index = False, encoding = "utf-8")  

