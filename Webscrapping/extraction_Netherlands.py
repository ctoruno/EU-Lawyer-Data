#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:48:27 2022

@author: carlostorunopaniagua
"""
#%%

# Libraries needed
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

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
driver = webdriver.Chrome(executable_path = '/Users/carlostorunopaniagua/Documents/GitHub/chromedriver_mac64',
                          options         = options)

#%%

N = 1

# Getting lawyer links from root pages
lawyer_links = []
for page in range(1, 5):
    print(N)
    N = N+1
    driver.get(f"https://zoekeenadvocaat.advocatenorde.nl/zoeken?q=&type=advocaten&limiet=10&sortering=naam&filters%5Brechtsgebieden%5D=%5B%5D&filters%5Bspecialisatieverenigingen%5D=%5B%5D&filters%5Btoevoegingen%5D=0&locatie%5Bstraal%5D=5&weergave=lijst&pagina={page}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content)

    for article in soup.findAll("div", class_ = "result advocaten"):
        for stags in article.findAll("span", class_ = "icon-before primary medium-down-expanded"):
            for atags in stags.findAll("a", href = True):
                print(atags["href"])
                lawyer_links.append(atags["href"])
            
#%%

# Saving links as CSV  
links = pd.DataFrame(lawyer_links)
links.to_csv("Netherlands/links_1-2500.csv", index = False, encoding = "utf-8")

#%%
# Extracting information from individual links
N = 1

lawyers_list = []
for link in lawyer_links:
    driver.get(f"https://zoekeenadvocaat.advocatenorde.nl{link}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    title_block     = soup.find("div", class_ = "title")
    name            = title_block.find("h3").text.strip()
    firm            = title_block.find("a", class_ = "secondary").text.strip()
    
    district = soup.find("a", class_ = "icon-after xsmall no-margin").find("span").text.strip()
    reg_date = soup.find("div", class_ = "icon-after small no-margin").find("span").text.strip()

    specializations = [] 
    specs_ls        = soup.find("div", class_ = "label-group").findAll("span")
    for spec in specs_ls:
        ex = spec.text.strip()
        specializations.append(ex)
    specializations = ", ".join(specializations)
    
    address_raw = []
    for a in soup.select(".medium-6 .no-margin-bottom"):
        c_address = a.text.strip()
        address_raw.append(c_address)
    address = "".join(address_raw).replace("\n", " ").replace(u'\xa0', u' ')
    
    telephone_list = []
    for ts in soup.select(".row:nth-child(8) a"):
        ts_element = ts.text.strip()
        telephone_list.append(ts_element)
    telephone = "; ".join(telephone_list)
    
    email_list = []
    for es in soup.select(".row:nth-child(10) a"):
        es_element = es.text.strip()
        email_list.append(es_element)
    email = "; ".join(email_list)
    
    web_list = []
    for ws in soup.select(".small-9 span"):
        ws_element = ws.text.strip()
        web_list.append(ws_element)
    website = "; ".join(web_list)
    
    lawyer = {
        "name"     : name,
        "firm"     : firm,
        "district" : district,
        "reg_date" : reg_date,
        "specs"    : specializations,
        "address"  : address,
        "phone"    : telephone,
        "email"    : email,
        "website"  : website 
        } 
    
    lawyers_list.append(lawyer)
    
    print(N)
    N = N+1

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Netherlands/Netherlands_batch1.csv", index = False, encoding = "utf-8")


