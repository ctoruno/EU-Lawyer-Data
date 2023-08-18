#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:21:07 2022

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

lawyers_list = []

#%%
# CASE 1

# function to get unique values
    
pages = ['v', 'g', 'd', 'e', 'z', 'i', 'th', 'i-2', 'l', 'n', 'ks', 'o', 'r','t', 'f', 'ch', 'ps']


for page in pages:
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-{page}/"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-{page}/")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")
    
    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)
        
#%%

# CASE 2

for page in range(0, 3):
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-a/?page_ff0af={page}"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-a/?page_ff0af={page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)   


#%%


# CASE 3

for page in range(0, 4):
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-k/?page_d17e5={page}"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-k/?page_d17e5={page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)   

#%%

# CASE 4

for page in range(0, 3):
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-m/?page_d601b={page}"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-m/?page_d601b={page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)   

#%%

# CASE 5

for page in range(0, 3):
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-p/?page_3d9fe={page}"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-p/?page_3d9fe={page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)   

#%%

# CASE 6

for page in range(0, 3):
    
    current_page = f"https://dspatras.gr/katalogos-melon-gramma-s/?page_bdb62={page}"
    print(current_page)
    driver.get(f"https://dspatras.gr/katalogos-melon-gramma-s/?page_bdb62={page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    for block in frame_soup.findAll("div", class_ = "um-member-card no-photo"):
        
        name_block     = block.find("div", class_ = "um-member-name")
        name           = name_block.find("a").text.strip()
        
        print(name)
        
        try:

            email_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-secondary_user_email")
            email           = email_block.find("a").text.strip()
        
        except AttributeError:
            
            email           = "NA"
        
        print(email)
        
        try:
            
            mobile_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-mobile_number")
            mobile           = mobile_block.find("a").text.strip()
        
        except AttributeError:
            
            mobile           = "NA"

        print(mobile)
        
        try:

            phone_block     = block.find("div", class_ = "um-member-tagline um-member-tagline-phone_number")
            phone           = phone_block.find("a").text.strip()
            
        except AttributeError:
            
            phone            = "NA"

        print(phone)
        
        try:

            address     = block.find("div", class_ = "um-member-tagline um-member-tagline-description").text.strip()
            
        except AttributeError:
            
            address      = "NA"

        print(address)
                    
        plink       = current_page
        print(plink)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "email"              : email,
            "mobile"             : mobile,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)   

#%%
master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Greece_Patras.csv", index = False, encoding = "utf-8")
