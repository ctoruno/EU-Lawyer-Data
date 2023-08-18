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
options.headless = False
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

#%%

N = 0

# function to get unique values
    
lawyer_links = []
for page in range (0,16):
    print(N)
    N = N+1
    driver.get(f"https://dsro.gr/katalogos-melon?sort_bef_combine=field_member_last_name_ASC&sort_by=field_member_last_name&sort_order=ASC&page={page}")
    time.sleep(10)
    driver.implicitly_wait(10)
    content = driver.page_source
    soup    = BeautifulSoup(content)
    
    for tags in soup.findAll("div", class_ = "views-field views-field-path"):
            for atags in tags.findAll("a", href = True):
                print(atags["href"])
                lawyer_links.append(atags["href"])
     
    print(N)          

#%%
unique_links = list(set(lawyer_links))
links = pd.DataFrame(lawyer_links)
links = links.drop_duplicates()

#%%
lawyers_list = []
#%%
# Extracting information from individual links
N = 0

#lawyers_list = []
for link in unique_links:
    driver.get(f"https://dsro.gr{link}")
    driver.implicitly_wait(10)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    try:
        name         = soup.find("div", class_ = "views-field views-field-field-member-name").text.strip()
    except AttributeError:
        name         = "NA"
    
    print(name)

    
    try:
        mobile       = soup.find("div", class_ = "views-field views-field-field-mobile-number").find("a").text.strip()
    except AttributeError:
        mobile      = "NA"

    print(mobile)

    try:
        phone        = soup.find("div", class_ = "views-field views-field-field-telephone-number").find("a").text.strip()
    except AttributeError:
        phone       = "NA"
        
    print(phone)

    
    try:
        address      = soup.find("div", class_ = "views-field views-field-field-address").text.strip()
    except AttributeError:
        address     = "NA"
        
    print(address)

    
    try:
        email        = soup.find("div", class_ = "views-field views-field-mail").find("a").text.strip()
    except AttributeError:
        email     = "NA"

    print(email)

    plink            = (f"https://dsro.gr{link}")
    print(plink)
    lawyer = {
        "name"       : name,
        "address"    : address,
        "mobile"     : mobile,
        "phone"      : phone,
        "email"      : email,
        "URL"        : plink
        } 
    
    lawyers_list.append(lawyer)
    N = N+1
    print(N)

#%%

master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Greece_Rhodope_315.csv", index = False, encoding = "utf-8")
