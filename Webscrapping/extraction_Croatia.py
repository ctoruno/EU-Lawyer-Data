#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 11:05:28 2022

@author: santiagopardo
"""

#%%

# Libraries needed
import time
import re
import names
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np


# Header definition
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

#%%
# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

#%%

N = 1

# function to get unique values
    
lawyer_links = []
for page in range (1,350):
    print(N)
    N = N+1
    driver.get(f"https://www.hok-cba.hr/imenik/?stranica={page}")
    time.sleep(3)
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content)
    
    for tags in soup.findAll("div", class_ = "directory-results-row"):
            for atags in tags.findAll("a", href = True):
                print(atags["href"])
                lawyer_links.append(atags["href"])
     
    print(N)          

#%%
unique_links = list(set(lawyer_links))
links = pd.DataFrame(lawyer_links)
links = links.drop_duplicates()

#links.to_csv("Croatia/links_1-350.csv", index = False, encoding = "utf-8")

#%%
lawyers_list = []
#%%
# Extracting information from individual links
N = 0

#lawyers_list = []
for link in unique_links:
    driver.get(f"{link}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    name         = soup.find("h1").text.strip()
    status       = soup.find("span", class_ = "entity-state").text.strip()
    
    try:
        phone        = soup.find("div", class_ = "entity-info entity-phone")
        phone        = phone.find("span").text.strip()
    except AttributeError:
        phone        = "NA"
    
    try:
        mobile       = soup.find("div", class_ = "entity-info entity-mobile")
        mobile       = mobile.find("a").text.strip()
    except AttributeError:
        mobile       = "NA"

    try:
        fax            = soup.find("div", class_ = "entity-info entity-fax").find("span").text.strip()
    except AttributeError:
        fax         = "NA"
    
    try:
        email       = soup.find("div", class_ = "entity-info entity-email").find("a").text.strip()
    except AttributeError:
        email       = "NA"
    
    try:
        languages = []
        title_block_idioms     = soup.find("div", class_ = "entity-info entity-languages").findAll("span")
        for idioms in title_block_idioms:
            lg = idioms.text.strip()
            languages.append(lg)
        languages = ",".join(languages)
    except AttributeError:
        languages       = "NA"
    
    try:
        address = []
        title_block_address     = soup.find("div", class_ = "entity-info entity-address").findAll("span")
        for ad in title_block_address:
            loc = ad.text.strip()
            address.append(loc)
        address = "-".join(address)
    except AttributeError:
        address       = "NA"
    
    plink            = link
    
    
    lawyer = {
        "name"       : name,
        "status"     : status,
        "address"    : address,
        "mobile"     : mobile,
        "phone"      : phone,
        "fax"        : fax,
        "email"      : email,
        "languages"  : languages,
        "URL"        : plink
        } 
    
    lawyers_list.append(lawyer)
    N = N+1
    print(N)


#%%

master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Croatia_6980.csv", index = False, encoding = "utf-8")


