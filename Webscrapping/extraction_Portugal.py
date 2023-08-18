#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:05:21 2022

@author: carlostorunopaniagua
"""
#%%

# Libraries needed
import time
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path = '/Users/carlostorunopaniagua/Documents/GitHub/chromedriver_mac64',
                          options         = options)

# Getting root website
url = "https://portal.oa.pt/advogados/pesquisa-de-advogados"
driver.get(url)

#%%

# Action sequence: Had trouble with identifying click element at the beginning
# action = ActionChains(driver)
# action.send_keys(Keys.ARROW_DOWN)
# action.send_keys(Keys.ENTER)
# action.perform()

# Click sequence: Actually, not necessary... URL is paginated and filter-oriented
# dropdown = driver.find_element_by_id("select2-conselho-regional-select-container")
# dropdown.click()

# Getting regions values
selection = driver.find_element_by_id("conselho-regional-select")
options = [x for x in selection.find_elements_by_tag_name("option")]
regions = [x.get_attribute("value") for x in options][1:]


#%%

# Setting up counter
N = 0 

# Creating an empty list to store results
lawyer_list = []

# Looping acroos regions and limited pages (records displayed stop at PAGE 6 ALWAYS)
for georeg in regions:
    for page in range(1,7):
        
        # Updating counter
        N = N + 10
        print(N)
        
        # Paginated link
        pag_url = f"https://portal.oa.pt/advogados/pesquisa-de-advogados?l=&cg={georeg}&ce=&n=&lo=&m=&cp=&a=on&op=&o=0&page={page}"
        driver.get(pag_url)
        time.sleep(3)
        
        # Fetching/Parsening
        content = driver.page_source
        soup    = BeautifulSoup(content, "lxml")
        
        # Looping across lawyers
        for block in soup.findAll("article", class_ = "search-results__article-person"):
            name_ele  = block.find("h4", class_ = "search-results__article-person-title")
            name      = name_ele.text.strip()
            status    = name_ele.find_parent("div").find_next_sibling("div").text.strip()   
            region    = block.find("span", text = "Conselho Regional").find_next_sibling("span").text.strip()  
            address   = block.find("span", text = "Localidade").find_next_sibling("span").text.strip() 
            
            try: 
                email     = block.find("span", text = "Email").find_next_sibling("span").text.strip() 
            except AttributeError:
                email     = "NA"
                continue
            
            try: 
                phone     = block.find("span", text = "Telefone").find_next_sibling("span").text.strip() 
            except AttributeError:
                telephone = "NA"
                continue
            
            # Defining dictionary entry
            lawyer = {
                "name"               : name,
                "status"             : status,
                "region"             : region,
                "address"            : address,
                "phone"              : phone,
                "email"              : email
                } 
            
            # Appending to main list
            lawyer_list.append(lawyer)


#%%        
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyer_list)
# master_data.to_csv("PORTUGAL.csv", index = False, encoding = "utf-8")