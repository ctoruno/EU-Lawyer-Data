#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:21:38 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path = '/Users/carlostorunopaniagua/Documents/GitHub/chromedriver_mac64',
                          options         = options)
# options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
# driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
#                           options         = options)

# Getting root website
url = "https://www.cyprusbar.org/CypriotAdvocateMembersPage"


#%%

# Defining starting/ending page
start_page   = 35
ending_page  = 35

# Creating an empty list to store data
lawyers_list = []

# Defining wait
wait = WebDriverWait(driver, 40)

# Setting up a cell counter

# Display 80 XPATH
d80_xpath     = '//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_DXPagerBottom_DDB"]'
li80_xpath    = '//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_DXPagerBottom_PSP_DXI3_T"]/span'

# Last page XPATH
page55_xpath  = '//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_DXPagerBottom"]/a[9]' 

# Previous page XPATH
pp_xpath      = '//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_DXPagerBottom"]/a[1]' 

#%%

# Looping across pages
for page in range(start_page, ending_page-1, -1):
    
    if page == 55:
        nrows = 5
    else:
        nrows = 81
    
    # Extracting info per page (every 80 rows we need to change page)
    for row in range(76, nrows):
        
        # Which cell are we?
        if page == 55:
            cell = ((page-1)*80)+(row-1)
        else:
            cell = (55*80)-((55-page+1)*80)+(row-1)
        
        # Getting root URL
        driver.get(url)
                
        # Displaying 80 records per page
        wait.until(EC.element_to_be_clickable((By.XPATH, d80_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, li80_xpath))).click()
        time.sleep(5)           
        
        # Getting to last page
        wait.until(EC.presence_of_element_located((By.XPATH, page55_xpath)))
        p55           = driver.find_element("xpath", page55_xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", p55)
        driver.execute_script("window.scrollBy(0, -150);")
        wait.until(EC.element_to_be_clickable((By.XPATH, page55_xpath))).click()
        time.sleep(4)
        
        # Locating current page (PREVIOUS PAGE clicks)
        bbar_xpath = '//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_DXPagerBottom"]'
        
        for i in range(55, page, -1):   
            # Clicking on PREVIOUS PAGE buttom
            wait.until(EC.presence_of_element_located((By.XPATH, pp_xpath)))
            pp = driver.find_element("xpath", pp_xpath)
            driver.execute_script("arguments[0].scrollIntoView(true);", pp)
            driver.execute_script("window.scrollBy(0, -150);")
            wait.until(EC.element_to_be_clickable((By.XPATH, pp_xpath))).click()
            time.sleep(4)
        
        # Clicking on corresponding lawyer
        details_xpath = f'//*[@id="ctl00_ContentPlaceHolder1_LawyersGrid_cell{cell}_0_btn_CD"]'
        wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details       = driver.find_element("xpath", details_xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", details)
        driver.execute_script("window.scrollBy(0, -150);")
        time.sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, details_xpath))).click()
        time.sleep(3)
        
        # Extracting information
        content = driver.page_source
        soup    = BeautifulSoup(content, "lxml")

        # Identifying panel with info and its rows
        panel   = soup.find("div", class_ = "panel panel-default")
        row     = panel.findAll("div", class_ = "row")
        
        # Extracting details into list
        detail = []
        for element in row:
            for item in element.findAll("tbody"):
                value = str(item.find("td", class_ = "dxic").find("input").get("value"))
                detail.append(value)
                
        # Defining elements        
        name     = detail[0]
        address  = detail[1]
        phone    = detail[3]
        district = detail[6]
        website  = detail[7]
        email    = detail[8]
        mobile   = detail[9]
        
        # Checking
        print("Extracting info from cell: " + str(cell) + ". Name: " + name)
        
        # Defining dictionary entry
        lawyer = {
            "name"               : name,
            "address"            : address,
            "phone"              : phone,
            "mobile"             : mobile,
            "email"              : email,
            "district"           : district,
            "website"            : website
            } 
        
        # Appending to main list
        lawyers_list.append(lawyer)
        
        # Updating cell
        cell = cell + 1
 
#%%

# Saving data
master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()
master_data.to_csv("Cyprus_10b.csv", index = False, encoding = "utf-8") 
