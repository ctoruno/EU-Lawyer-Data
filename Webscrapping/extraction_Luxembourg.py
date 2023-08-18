#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:12:05 2022

@author: carlostorunopaniagua
"""
#%%

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

# Defining root_URL to extract links
url = ["https://www.barreau.lu/searchbypreferentialactivity?p_p_id=avocatsearchbypreferentialActivity_",
       "WAR_avocatportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_",
       "count=1&_avocatsearchbypreferentialActivity_WAR_avocatportlet_preferentialActivityParam=&_",
       "avocatsearchbypreferentialActivity_WAR_avocatportlet_delta=10&_avocatsearchbypreferential",
       "Activity_WAR_avocatportlet_keywords=&_avocatsearchbypreferentialActivity_WAR_avocatportlet_", 
       "advancedSearch=false&_avocatsearchbypreferentialActivity_WAR_avocatportlet_andOperator=true&_",
       "avocatsearchbypreferentialActivity_WAR_avocatportlet_resetCur=false&_avocatsearchbypreferential",
       "Activity_WAR_avocatportlet_"]

root_url     = "".join(url)

# Creating an empty list to store results
lawyer_links = []

# Looping across pages
for page in range(1,326):
    
    print("Currently extracting links from page " + str(page) + " of 325")
    page_url = root_url + f"cur={page}"
    
    # Fetching/parsening
    response = requests.get(page_url,
                            headers = headers)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(2)
    
    # Looping across table rows        
    for rows in soup.find("tbody", class_ = "table-data").findAll("tr"):
        try:
            link = (rows.findChild("td").find("a", href = True))["href"]
            lawyer_links.append(link)
        except TypeError:
            continue
        
#%%

# Saving links as CSV  
linksDF = pd.DataFrame(lawyer_links).drop_duplicates()
linksDF.to_csv("Luxembourg_links.csv", index = False, encoding = "utf-8")

# Reading links CSV
lawyer_links = pd.read_csv("Luxembourg_links.csv")["0"].tolist()     


#%%

# Setting up a counter
N = 2221

# Creating an empty list to store data
# lawyers_list = []

# Looping across links
for item in lawyer_links[N:]:
    
    print(N)
    plink = "https://www.barreau.lu/" + item
    
    # Fetching/parsening
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(3)
    
    # Retrieving elements
    column_block = soup.find("div", {"id": "column-2"})    
    info_block   = column_block.find("div", class_ = "portlet-body")
    
    name      = info_block.find("h1").text.strip()
    firm_name = info_block.find("h2", string = re.compile("Etude")).find_next_sibling("p").text.strip()
    address   = [info_block.find("h2", string = re.compile("Adresse")).find_next_sibling("p").text.strip(),
                 info_block.find("h2", string = re.compile("Adresse")).find_next_sibling("p").find_next_sibling("p").text.strip()]
    address   = " ".join(address)
    phone     = info_block.find("p", string = re.compile("Téléphone de l'étude")).find_next_sibling("p").text.strip()
    reg_date  = info_block.find("p", string = re.compile("Prestation de serment")).text.strip()
    reg_date  = re.search("(?<=serment\s:\s).+", reg_date).group()
    
    try: 
        website   = info_block.find("a", href = True)["href"]
    except TypeError:
        website   = "NA"
        
    try: 
        specs     = info_block.find("div", {"id": "printable"}).text.strip()
        specs     = re.search("(?<=Activités préférentielles).+$", specs).group()
    except AttributeError:
        specs     = "NA"

    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "reg_date"           : reg_date,   
        "specializations"    : specs,
        "address"            : address,
        "phone"              : phone,
        "firm_name"          : firm_name,
        "firm_website"       : website,
        "URL"                : plink
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Upddating counter
    N = N + 1
 
    
#%%   
     
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Luxembourg.csv", index = False, encoding = "utf-8")        
        
        


    