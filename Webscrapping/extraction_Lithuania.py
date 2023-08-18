#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:29:47 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

#%%

# WARNING: website has a rate-limit per day

# Getting root website to extract individual links
root_url = "https://www.advokatura.lt/irasai/advokatu-paieska/"
driver.get(root_url)
time.sleep(5)

# Defining wait:
wait = WebDriverWait(driver, 10)

# Defining action sequence to navigate across specializations
action = ActionChains(driver)
action.send_keys(Keys.ARROW_DOWN)
action.send_keys(Keys.ENTER)

# Accepting cookies (No idea if this happens in a headless browser)
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[1]/a'))).click()

# Creating an empty list to store links
lawyers_links = []

# Retrieving number of specializations
ddown = driver.find_element_by_xpath('//*[@id="page"]/main/section[3]/div[1]/div/aside/div[1]/form/div/div[4]/div/select')
nopts = len(Select(ddown).options[1:])

# Looping across specializations
for i in range(0, nopts):
    
    # Selecting specialization
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page"]/main/section[3]/div[1]/div/aside/div[1]/form/div/div[4]/div/span/span[1]/span/span[2]'))).click()
    action.perform()
    category = driver.find_element_by_xpath('//*[@id="page"]/main/section[3]/div[1]/div/aside/div[1]/form/div/div[4]/div').text
    print("Extracting data from specialization: " + category)
    time.sleep(2)
    
    # Clicking on DISPLAY 100 items buttom
    if i == 0:
        # DISPLAY 100 ONCE
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page"]/main/section[3]/div[1]/div/div/div[1]/div[2]/div[4]'))).click()
        time.sleep(2)
    
    # Length of elements inside tag that contains the NEXT PAGE buttom 
    npages = len(driver.find_elements_by_xpath('//*[@id="page"]/main/section[3]/div[1]/div/div/div[3]/div[2]/div/ul/li'))-1
    if npages == -1:
        npages = 1
        
    print("Specializations has " + str(npages) + " pages to navigate through")    
    
    # Looping across pages within specialization
    for page in range(1, npages+1):
        print("Currently extracting data from page: " + str(page))
    
        # Extracting links
        content = driver.page_source
        soup    = BeautifulSoup(content, "lxml")
        
        for element in soup.findAll("div", class_ = "search-people-item"):
            href = element.find("div", class_ = "contact-info").find("div", class_ = "selected").find("a", href = True)["href"]
            print(href)
            lawyers_links.append(href)
    
        # Setting a personalized index for the location of the NEXT PAGE buttom within its parent tag
        if page == 1:
            index = npages + 1
        else:
            index = npages + 2
        
        if page < npages:
            # We use this index to click on the NEXT PAGE buttom
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="page"]/main/section[3]/div[1]/div/div/div[3]/div[2]/div/ul/li[{index}]/a'))).click()
            
        time.sleep(2)
  
#%%

# Closing driver
driver.quit()

# Saving links as CSV  
links = pd.DataFrame(lawyers_links).drop_duplicates()
links.to_csv("Lithuania_links.csv", index = False, encoding = "utf-8")

# Reading links CSV
# test = pd.read_csv("Lithuania_links.csv")["0"].tolist()
    
#%%

# Setting up a counter

lawyers_links = lawyers_links.values.tolist()
lawyers_links = [re.sub("\[|\]|'", "", str(element)) for element in lawyers_links]

N = 938

# Creating an empty list to store data
#lawyers_list = []

# Looping across links
for item in lawyers_links[N:1720]:
    
    print(N)
    plink = item
    
    # Fetching/parsening
    response = requests.get(plink)
    soup     = BeautifulSoup(response.text, "lxml")
    time.sleep(3)
    
    # Retrieving elements
    name = soup.find("div", class_ = "custom-title-1 semi-black-color").text.strip()
    
    bio  = re.sub("\s\s", "", re.sub("\n","<>", soup.find("div", class_ = "bio").text.strip()))
    
    try: 
        phone   = " - ".join(re.findall("\+37.+?(?=<>)", bio))
    except AttributeError:
        phone   = "NA"
    
    try: 
        email   = re.search("((?<=^)|(?<=<>))(?:(?!<>).)+@.+?(?=<>)", bio).group()
    except AttributeError:
        email   = "NA"
    
    try: 
        address = re.search("(?<=<>)(?:(?!<>).)+(?=Kalba)", re.sub("[<>]*(?=Kalba)","", bio)).group()
    except AttributeError:
        try: 
            address = re.search("(?<=<>)(?:(?!<>).)+(?=Rašyti)", re.sub("[<>]*(?=Rašyti)","", bio)).group()
        except AttributeError:
            address = "NA"
    
    try: 
        langs   = re.sub("<>", "", re.search("(?<=Kalba:).+(?=Rašyti)", bio).group())
    except AttributeError:
        langs   = "NA"
    
    firm_info = soup.find("div", class_ = "pure-u-1-1 pure-u-md-1-3")
    
    try: 
        firm_contacts = re.sub("\n", "<>", firm_info.find("div", class_ = "contact-info-right").text.strip())
    except AttributeError:
        firm_contacts = "NA"
        
    firm_name    = firm_info.find("div", class_ = "custom-title-2 semi-black-color").text.strip()
    firm_phone   = " - ".join(re.findall("\+37.+?(?=<>)", firm_contacts))
    
    try: 
        firm_email   = re.search("((?<=^)|(?<=<>))(?:(?!<>).)+@.+?((?=<>)|(?=$))", firm_contacts).group()
    except AttributeError:
        firm_email   = "NA"
    
    try: 
        firm_website = re.search("http.+", firm_contacts).group()
    except AttributeError:
        firm_website = "NA"
    
    try: 
        indepth_info = soup.find("div", class_ = "full-info")
    except AttributeError:
        indepth_info = "NA"
    
    specs        = re.sub("\n\n\n", "<>", re.sub("  ", "", indepth_info.find("ul").text.strip()))
    reg_date     = re.search("(?<=nuo:\s).+", indepth_info.find("div", string = re.compile("praktika nuo")).text.strip()).group()
    
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "reg_date"           : reg_date,   
        "specializations"    : specs,
        "address"            : address,
        "phone"              : phone,
        "email"              : email,
        "firm_name"          : firm_name,
        "firm_phone"         : firm_phone,
        "firm_email"         : firm_email,
        "firm_website"       : firm_website,
        "languagues"         : langs,
        "URL"                : plink
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    # Upddating counter
    N = N + 1

#%%   
     
# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("/Users/santiagopardo/Documents/Lithuania.csv", index = False, encoding = "utf-8") 



