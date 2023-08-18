#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 07:43:35 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import pandas as pd
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
options.headless = True
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

# Getting root website
url = "https://ouny.magyarugyvedikamara.hu/licoms/common/service/requestparser?name=pubsearcher&action=search&type=ugyved&status=aktiv&p=2"
driver.get(url)

#%%

# Selecting lawyers data in website
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nyilvanos-tipusok"]/div/div/div[1]/div/div'))).click()

# Waiting for deployable options to be displayed
wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[(@id = "iFrameResizer0")]')))
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchForm"]/div[2]/div')))
time.sleep(5)

# Searching ALL lawyers
driver.switch_to.default_content()
search_button = driver.find_element_by_xpath('//*[@id="pubsearcher"]/div[4]/div[1]')
search_button.click()
time.sleep(5)

# Action sequence (I was using this keyboard sequence to select and click the SEARCH button before locating iFrame)
# action = ActionChains(driver)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.TAB)
# action.send_keys(Keys.ENTER)
# action.perform()

#%%

# Getting current list source code
content = driver.page_source
soup    = BeautifulSoup(content)

# Accesing the iFrame source code
iframe_src = soup.select_one("#iFrameResizer1").attrs["src"]

# Retrieving iFrame standar paginated URL
driver.get(f"https:{iframe_src}")
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/ul/li[12]/a'))).click()

new_url = driver.current_url[:len(driver.current_url)-1]


#%%

# Defining an empty list for lawyers
lawyers_list = []

# Setting a counter
N = 0

# Setting-up a for loop to scrap through pagination
for page in range(1, 474):
    N = N + 25
    print(N)
    current_page = f"{new_url}{page}"
    print(current_page)
    driver.get(f"{new_url}{page}")
    time.sleep(5)    
    frame_content = driver.page_source
    frame_soup    = BeautifulSoup(frame_content, "lxml")

    # Retrieving info for each lawyer
    for block in frame_soup.findAll("div", class_ = "media-body"):
        name      = block.select_one('div > div:nth-child(3) > div > p').text.strip()
        KASZ_ID   = block.select_one('div > div:nth-child(2) > div > p').text.strip()
        status    = block.select_one('div > div:nth-child(4) > div > p').text.strip()
        chamber   = block.find("label", text="KAMARA *").find_next_sibling("div").find("p").text.strip()
        
        try: 
            email     = block.find("label", text="E-MAIL *").find_next_sibling("div").find("p").text.strip()
        except AttributeError:
            email     = "NA"
            # continue
        
        try: 
            languages = block.select_one('div > div:nth-child(7) > div > p').text.strip()
        except AttributeError:
            languages = "NA"
            # continue
        
        try: 
            address   = block.find("label", text="CÍME *").find_next_sibling("div").find("p").text.strip()
        except AttributeError:
            address   = "NA"
            # continue
        
        try: 
            telephone = block.find("label", text="TELEFONSZÁMA *").find_next_sibling("div").find("p").text.strip()
        except AttributeError:
            telephone = "NA"
            # continue
        
        try: 
            specs     = block.find("label", text="JOGTERÜLET *").find_next_sibling("div").find("p").text.strip()
        except AttributeError:
            specs     = "NA"
            # continue
        
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "KASZ_ID"            : KASZ_ID,
            "status"             : status,
            "chamber"            : chamber,
            "specializations"    : specs,
            "address"            : address,
            "phone"              : telephone,
            "email"              : email,
            "languagues"         : languages
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)
    
    
#%%        

# Closing driver
driver.close()

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Hungary_11319.csv", index = False, encoding = "utf-8")

