#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 20:53:59 2022

@author: santiagopardo
"""

#%%

# Libraries needed
import time
import pandas as pd
import re

# import requests
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)
#%%

# Getting root website
url = "https://www.ifep.ro/Justice/Lawyers/LawyersPanel.aspx"
driver.get(url)
lawyers_list =[]

#%%
for i in range (9):
    
# Selecting lawyers data in website
    time.sleep(5)
    
    # Getting current list source code
    content = driver.page_source
    soup    = BeautifulSoup(content)
    
    for block in soup.findAll("div", class_ = "col-md-12"):
        try:
            name        = block.find("span", class_ = "label label-info").find_next_sibling("font").text.strip()
        except AttributeError:
            try :
                name    = block.find("span", class_ = "label label-success").find_next_sibling("font").text.strip()
            except AttributeError:
                name     = "NA"
        try:
            active       = block.find("span", class_ = "label label-info").find_next_sibling("span").text.strip()
        except AttributeError:
            try :
                active   = block.find("span", class_ = "label label-success").find_next_sibling("span").text.strip()
            except AttributeError:
                active   = "NA"
        
        try:
            address_block    = block.find("span", class_ = "fas fa-map-marker text-red padding-right-sm").find_parent().text.strip()
        except AttributeError:
            address_block    = "NA"
            
        try:
            address       = re.search("(?<=adresă:\s).+", address_block).group()
        except AttributeError:
            address       = "NA"
            
        try:
            bar           = re.search("^([^,])+", address_block).group()
        except AttributeError:
            bar           = "NA"
                
        try:
            email         = block.find("span", class_ = "text-nowrap").text.strip()
        except AttributeError:
            email         = "NA"
        
        try:
            phone         = block.find("span", class_ = "fal fa-phone text-primary padding-right-sm").find_parent().text.strip()
        except AttributeError:
            phone         = "NA"
        
        lawyer = {
            "name"       : name,
            "status"     : active,
            "bar"        : bar,
            "address"    : address,
            "phone"      : phone,
            "email"      : email,
            }
        lawyers_list.append(lawyer)
        
    driver.find_element(By.XPATH, '//*[@id="MainContent_PagerTop_NavNext"]').click()
    time.sleep(5)
    print(i)
    print(len(lawyers_list))

#%%

master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Rumania2_36810.csv", index = False, encoding = "utf-8")

