#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:26:13 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import re
import pandas as pd
import requests
import names
from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

# Getting root website to extract individual links
url = ["https://www.rechtsanwaelte.at/en/support-and-services/services/find-a-lawyer/?tx_rafinden_simplesearch",
       "%5Baction%5D=fullList&tx_rafinden_simplesearch%5Bcontroller%5D=LawyerSearch&cHash=1253f15e9a31b8feb9051",
       "f1d04cf144f"]
driver.get("".join(url))
time.sleep(15)

#%%

# Fetching/Parsening
content = driver.page_source
soup    = BeautifulSoup(content)
driver.close()

# Looping across lawyers to get individual url
lawyer_links = [blocks.find("a", href = True)["href"]
                for blocks in soup.findAll("div", class_ = "item grey rounded bottomMargin4")]

# Saving links as CSV  
links = pd.DataFrame(lawyer_links)
links.to_csv("Austria_links.csv", index = False, encoding = "utf-8")

#%%

# Initial header definition
agent = ["Noemi Sanchez using Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

# Setting up a counter
N = 0
X = 49

# Creating an empty list to store results
lawyers_list = []

# Looping across retrieved links
for link in lawyer_links[N:6926]:
    
    # Current count
    print(N)
    print("Requests until boom:" + str(X))
    
    # Testing reset
    if X == 0:
        
        # Generating new random name for User-Agent
        random_name = names.get_full_name()

        # Header definition
        agent = [random_name,
                 " using Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
                 "96.0.4664.110 Safari/537.36. "]
        headers = {
            "User-Agent": "".join(agent)
        }
        
        # Reseting counter
        X = 49
        time.sleep(60)
    
    # Getting url
    # driver.get(f"https://www.rechtsanwaelte.at{link}")
    response = requests.get(f"https://www.rechtsanwaelte.at{link}", 
                            headers = headers)
    X = X - 1
    time.sleep(2)
    
    # Fetching/Parsening
    # record_content = driver.page_source
    record_soup    = BeautifulSoup(response.text, "lxml")
    
    # Retrieving information
    name            = record_soup.find("span", class_ = "lastname").text.strip()
    address         = "-".join([ftags.text.strip() for ftags in record_soup.find(id = "tm").contents])
    
    contact_data    = record_soup.find("ul", class_ = "lawywer-search")
    
    try: 
        phone       = contact_data.findChild("li").text.strip()
    except AttributeError:
        phone       = "NA"
        
    try: 
        email       = contact_data.find("li", class_ = "email").find("a").text.strip()
    except AttributeError:
        email       = "NA"
        
    try: 
        website     = contact_data.find("li", class_ = "email").find_next_sibling("li").find("a").text.strip()
    except AttributeError:
        website     = "NA"
    
    # tbody           = record_soup.find("tbody")
    # info = []
    # for items in tbody.findAll("tr"):
    #     elements = items.findAll("td")
    #     for tagies in elements:
    #         chunk = tagies.text
    #         info.append(chunk)
    # full_info = "-".join(info)
    
    try: 
        reg_number = record_soup.find("td", string = re.compile("Lawyers")).find_next_sibling("td").text.strip()
    except AttributeError:
        reg_number = "NA"
        
    try: 
        firm       = record_soup.find("td", string = re.compile("Law firm:")).find_next_sibling("td").text.strip()
    except AttributeError:
        firm       = "NA"
    
    try: 
        specs      = str(record_soup.find("td", string = re.compile("Areas of work")).find_next_sibling("td"))
    except AttributeError:
        specs      = "NA"
    
    try: 
        langs      = record_soup.find("td", string = re.compile("Language")).find_next_sibling("td").text.strip()
    except AttributeError:
        langs      = "NA"

    
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "reg_number"         : reg_number,
        "specializations"    : specs,
        "address"            : address,
        "firm"               : firm,
        "phone"              : phone,
        "email"              : email,
        "website"            : website,
        "languagues"         : langs
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Upddating counter
    N = N + 1
    
#%%   
     
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Austria_2926.csv", index = False, encoding = "utf-8") 
