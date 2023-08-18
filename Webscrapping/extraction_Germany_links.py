#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri December 9 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path = "/Users/carlostorunopaniagua/Documents/GitHub/chromedriver_mac64",
                          options         = options)

# Defining a waiting period
wait = WebDriverWait(driver, 10)

#%%

# Getting root website to extract individual links
root_url = "https://anwaltauskunft.de/anwaltssuche"
driver.get(root_url)

# Sorting lawyers by alphabetical order
dropdown  = Select(driver.find_element_by_id("ls_sort_sort"))
dropdown.select_by_value("lawyer_name")

# Creating an empty list to store results
lawyers_links = []

#%% 

# Loopinga across pages
for page in range(1, 5866):

    # Fetching/Parsening
    print("Currently extracting links from page " + str(page))
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")

    # Extracting links
    card_body = soup.find("div", class_ = "card-body p-0")
    results   = [card.find("a").get("href") for card 
                    in card_body.findAll("div", class_ = "lawyer lawyer-list")]
    
    # Storing links
    lawyers_links.extend(results)

    # Defining NEXT PAGE xpath
    if page == 1:
        nextpath = '//*[@id="article-12"]/div[1]/div[2]/div[3]/nav/ul/li[8]/a'
    if page == 2:
        nextpath = '//*[@id="article-12"]/div[1]/div[2]/div[3]/nav/ul/li[9]/a'
    if page > 2:
        nextpath = '//*[@id="article-12"]/div[1]/div[2]/div[3]/nav/ul/li[10]/a'
    
    # Clicking on the next page
    if page < 5865:
        wait.until(EC.element_to_be_clickable((By.XPATH, nextpath))).click()

#%%

# Saving links as CSV  
links = pd.DataFrame(lawyers_links).drop_duplicates()
links.to_csv("Germany_links.csv", index = False, encoding = "utf-8")
