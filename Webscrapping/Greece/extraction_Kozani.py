#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:42:37 2022

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

# function to get unique values
lawyer_links = []
driver.get(f"https://dsk.gr/member_list/")
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="154"]/div/div[3]/a[7]'))).click()


for page in range (1,7):
    
    N = page+1
    driver.implicitly_wait(5)
    content = driver.page_source
    soup    = BeautifulSoup(content)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="154"]/div/div[3]/a[2]'))).click()


    for tags in soup.findAll("div", class_ = "upme-field-name"):
        for atags in tags.findAll("a", href = True):
            print(atags["href"])
            lawyer_links.append(atags["href"])
            print(N)          
#%%
unique_links = list(set(lawyer_links))
links = pd.DataFrame(lawyer_links)
links = links.drop_duplicates()

#%%
#%%
# Extracting information from individual links

lawyers_list = []

N = 0

for link in unique_links:
    driver.get(f"{link}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    name    = soup.find("div", class_ = "upme-field-name").text.strip()
    print(name)
    
    try:
        address_block = soup.find("div", class_ = "upme-field upme-view upme-dsk_address")
        address = address_block.find("div", class_ = "upme-field-value").text.strip()
        address_final = re.search("^.*?(?=ops!)", address).group()
    except AttributeError:
        address_final        = "NA"
    
    print(address_final)
   
    try:
        phone_block = soup.find("div", class_ = "upme-field upme-view upme-dsk_phone_office")
        phone       = phone_block.find("div", class_ = "upme-field-value").text.strip()
        
    except AttributeError:
        phone        = "NA"
        
    print(phone)
    

    try:
        mobile_block = soup.find("div", class_ = "upme-field upme-view upme-dsk_mobile")
        mobile       = mobile_block.find("div", class_ = "upme-field-value").text.strip()
        
    except AttributeError:
        mobile = "NA"
    
    print(mobile)
    
    try:
        fax_block = soup.find("div", class_ = "upme-field upme-view upme-dsk_fax")
        fax       = fax_block.find("div", class_ = "upme-field-value").text.strip()
        
    except AttributeError:
        fax = "NA"
        
    print(fax)
    
    try:
        email_block = soup.find("div", class_ = "upme-field upme-view upme-dsk_email")
        email       = email_block.find("div", class_ = "upme-field-value").text.strip()
        
    except AttributeError:
        email = "NA"
        
    print(email)
    
    plink = link
    
    lawyer = {
        "name"       : name,
        "address"    : address_final,
        "mobile"     : mobile,
        "phone"      : phone,
        "fax"        : fax,
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
master_data.to_csv("Greece_Kozani.csv", index = False, encoding = "utf-8") 

    