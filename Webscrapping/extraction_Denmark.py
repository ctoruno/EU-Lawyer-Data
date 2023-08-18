#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 08:16:11 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import re
import pandas as pd
import requests
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
options.headless = True
driver = webdriver.Chrome(executable_path = "/Users/carlostorunopaniagua/Documents/GitHub/chromedriver_mac64",
                          options         = options)

#%%

# Getting root website to extract individual links
root_url = "https://www.advokatnoeglen.dk/"
driver.get(root_url)

# Getting regions values and names into a dictionary
dropdown       = driver.find_element_by_id("ContentPlaceHolder_Search_CourtSelect")
regions_names  = [region.text for region in  Select(dropdown).options][1:]
regions_values = [x.get_attribute("value") for x in dropdown.find_elements_by_tag_name("option")][1:]

regions        = {regions_names[i]:regions_values[i] for i in range(len(regions_names))}

#%%

# Defining a waiting period
wait = WebDriverWait(driver, 10)

# Accepting cookies
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonAcceptWrapper"]'))).click()

# Creating an empty list were we will save the extracted links
link_list = []

# Iterating through dictionary tuples:
for region, code in regions.items():
    print("Retrieving links from region: " + region + " (code:" + code + ")")
    
    # Retrivieng code from page
    time.sleep(2)
    driver.get(f"https://www.advokatnoeglen.dk/sog.aspx?s=1&t=0&c={code}")
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    N = 1
    print("Currently extracting links of page: " + str(N))
    
    for element in soup.findAll("tr"):
        try:
            if re.match('location.href',element['onclick']):    
                link = re.search("(?<=location\.href=').+(?=')", element['onclick']).group()
                link_list.append(link)
        except:pass
    
    while True:
        try :
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Næste"))).click()
            N = N + 1
            content = driver.page_source
            soup    = BeautifulSoup(content, "lxml")
            print("Currently extracting links of page: " + str(N))
            
            for element in soup.findAll("tr"):
                try:
                    if re.match('location.href',element['onclick']):    
                        link = re.search("(?<=location\.href=').+(?=')", element['onclick']).group()
                        link_list.append(link)
                except:pass
            
        except TimeoutException:
            print("No next page for this region")
            break
    
#%%

# Opening links from CSV
# import csv
# with open('Denmark_links.csv', newline='') as f:
#     reader = csv.reader(f)
#     link_list = list(reader)[1:]
# link_list = [re.sub("\[|\]|'", "", str(element)) for element in link_list]

# Saving links as CSV  
links = pd.DataFrame(link_list)
links.to_csv("Denmark_links.csv", index = False, encoding = "utf-8")

#%%

# Header definition
agent = ["Carlos Toruno (carlos.a.torunop@gmail.com) using ",
         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

# Setting-up a counter
N = 0

# Creating an empty list to save extracted data
lawyers_list = []

#%%
    
# Extracting information from individual links
for link in link_list[N:3001]:
    print(N)
    plink       = f"https://www.advokatnoeglen.dk{link}"
    response    = requests.get(plink, headers = headers)
    time.sleep(3) 
    # content = driver.page_source
    soup        = BeautifulSoup(response.text, "lxml")   
    
    person      = soup.find("div", class_ = "person")
    name        = person.find("h1").text.strip()
    title       = person.find("h1").find_next_sibling().text.strip()
    specs       = person.select_one("div+ h2").text.strip()
    
    try:
        specs       = re.search("(?<=Arbejdsområder:\s).+", specs).group().strip()
    except AttributeError:
        specs       = "NA"
    
    lawyer_info = person.select_one("div+ h2").find_next_sibling().text.strip()
    lawyer_info = re.sub(" ", "", lawyer_info)
    lawyer_info = "<>".join(re.sub("\n\n", "\n", lawyer_info).split("\n"))
    
    try:
        email1  = re.search("(?<=e\=).+", soup.select_one(".person h2+ p a", href = True).get("href")).group()[::-1]
    except AttributeError:
        email1  = "NA"
    try:
        email2  = re.search("(?<=E-mail).+(?=Mobil)", lawyer_info).group()
    except AttributeError:
        email2  = "NA"
    
    reg_date    = re.search("(?<=Beskikkelsesår:).+?(?=(<>|$|\r))", lawyer_info).group()
    phone       = re.search("(?<=Mobiltlf).+", lawyer_info).group()
    if phone == ".:":
        phone = "NA"
    
    firm_info   = person.select_one("div+ h2").find_next_sibling().find_next_sibling()
    firm        = firm_info.select_one("h2").text.strip()
    
    g_info      = [element.text.strip() for element in firm_info.findAll("p")]
    g_info      = re.sub("  |\r|\n", "", "<>".join(g_info))
    g_info      = re.sub("\r|\n", "<>", g_info)
    
    address     = re.sub("<><>"," ",re.search(".+?(?=Danmark)", g_info).group())
    phone       = re.search("(?<=Tlf\.:\s).+?(?=(<>|Fax))", g_info).group()
    
    try:
        firm_email1  = re.search("(?<=e\=).+", firm_info.select_one("a", rel = True, href = True).get("href")).group()[::-1]
    except AttributeError:
        firm_email1  = "NA"
    try:
        firm_email2 = re.search("(?<=Email:\s).+?(?=<>)", g_info).group()
    except AttributeError:
        firm_email2  = "NA"

    try:
        website = re.search("www\..+\.(com|dk)", g_info).group()
    except AttributeError:
        website = "NA"
    
    district    = re.search("(?<=Retskreds:\s).+?(?=(\s|$))", g_info).group()
    
    # Defining dictionary entry
    lawyer = {
        "name"               : name,
        "URL"                : plink,
        "title"              : title,
        "district"           : district,
        "specializations"    : specs,
        "address"            : address,
        "phone"              : phone,
        "email1"             : email1,
        "email2"             : email2,
        "reg_date"           : reg_date,
        "firm_name"          : firm,
        "firm_email1"        : firm_email1,
        "firm_email2"        : firm_email2,
        "website"            : website
        } 
    
    # Appending to main list
    lawyers_list.append(lawyer)
    
    N = N + 1
       
#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Denmark_batch2.csv", index = False, encoding = "utf-8")
    