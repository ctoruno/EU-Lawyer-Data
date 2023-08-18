#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:03:05 2022

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
options.headless = False
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)
#%%

N = 0

# function to get unique values
    
lawyers_list = []
pages = ['a-b-c', 'd-e-z-h-th-i', 'k-l', 'm-n-x-o', 'p-r', 's-t-y', 'ph-x-ps-w']

for page in pages:
    N = N+1
    current_page = f"http://www.dsreth.gr/index.php/arxiki/ta-melh/{page}"
    print(current_page)
    driver.get(f"http://www.dsreth.gr/index.php/arxiki/ta-melh/{page}")
    time.sleep(10)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")
    
    tbody         = frame_soup.find("div",class_="item-page clearfix")
    
    for block in tbody.findAll("tr"):
        
        try:
            name    = block.find("td").text.strip()
            name    = re.sub("\n", ";", name)
            name    = re.match("^[^;]*", name).group().strip()    
        except AttributeError:
            name         = "NA"
            
        print(name)
    
        
        try:
            email   = block.find("td").find_next_sibling("td")
            email   = email.find("a").text.strip()
        except AttributeError:
            email         = "NA"
            
        print(email)
     
        
        try:
            phone   = block.find("td").find_next_sibling("td")
            phone   = phone.text.strip()
            phone   = re.sub("\n", ";", phone)
            phone   = re.sub(".:", " ", phone)
            phone   = re.search("(?<=Τη).*$", phone).group()
            phone   = re.match("^[^;]*", phone).group()
            phone   = re.sub(",", "", phone).strip()
            phone   = re.sub("[^0-9]", "", phone)
        except AttributeError:
            phone         = "NA"
        
        print(phone)
    
        
        try:
            fax    = block.find("td").find_next_sibling("td")
            fax    = fax.text.strip()
            fax    = re.sub("\n", ";", fax)   
            fax    = re.search("(?<=κιν. ).*$", fax).group().strip()
            fax    = re.sub("[^0-9]", "", fax)
        except AttributeError:
            fax         = "NA"
        
        print (fax)
    
        try:
            address    = block.find("td").text.strip()
            address    = re.sub("\n", ";", address)
            address    = re.search(";([^;]*)([^;]*);", address).group()
            address    = re.sub(";", "", address).strip()
            address    = f"{address}, Rethymno"
        except AttributeError:
            address         = "NA"
        
        print(address)
    
        
        plink      = current_page
        
    
    
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "fax"                : fax,
            "email"              : email,
            "link"               : plink
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)
#%%

master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Greece_Rethymno_178.csv", index = False, encoding = "utf-8")
