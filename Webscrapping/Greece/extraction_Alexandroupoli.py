#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 08:28:46 2022

@author: santiagopardo
"""

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
for page in range (0,13):
    print(N)
    N = N+1
    driver.get(f"https://www.dsaxd.gr/members/home/page:{page}")
    time.sleep(3)
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content)
    
    for tags in soup.findAll("div", class_ = "member"):
            for atags in tags.findAll("a", href = True):
                print(atags["href"])
                lawyer_links.append(atags["href"])
    print(N)          
#%%
unique_links = list(set(lawyer_links))
links = pd.DataFrame(lawyer_links)
links = links.drop_duplicates()
#%%
# Extracting information from individual links

lawyers_list = []

N = 0

for link in unique_links:
    driver.get(f"https://www.dsaxd.gr{link}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    name       = soup.find("h1", class_ = "bg_black aos-init aos-animate").text.strip()
    print(name)
    
    try:
        phone_block   = soup.find("p", class_ = "member_icon member_phone").text.strip()
        phone         = re.search("[^ :]+$", phone_block).group()
        
    except AttributeError:
        phone         = "NA"
        
    print(phone)
    
    try:
        mobile_block   = soup.find("p", class_ = "member_icon member_mobile").text.strip()
        mobile         = re.search("[^ :]+$", mobile_block).group()
        
    except AttributeError:
        mobile         = "NA"  
    
    print(mobile)
    
    try:
        email_block   = soup.find("p", class_ = "member_icon member_email").text.strip()
        email         = re.search("[^ :]+$", email_block).group()
        
    except AttributeError:
        email       = "NA"
        
    print(email)
    

    try:
        address_block = soup.find("p", class_ = "member_icon member_address").text.strip()
        address       = re.search("(?<=\: ).*", address_block).group()
        
    except AttributeError:
        address       = "NA"
        
    print(address)
    
    plink      = f"https://www.dsaxd.gr{link}"
    print(plink)
    
    lawyer = {
        "name"       : name,
        "address"    : address,
        "mobile"     : mobile,
        "phone"      : phone,
        "email"      : email,
        "URL"        : plink
        } 
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Upddating counter
    N = N + 1
    
    print(N)
    #%%          
# Saving data into a dataframe  
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Greece_Alexandroupoli.csv", index = False, encoding = "utf-8") 
