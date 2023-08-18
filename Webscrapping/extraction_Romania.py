#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 21:11:20 2022

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

links = pd.read_excel (r'/Users/santiagopardo/Library/CloudStorage/OneDrive-Bibliotecascompartidas:WorldJusticeProject/Research - Data Analytics/4. EU Subnational/Webscrapping/Data/DATA_RAW/Romania/links_rumania_4.xlsx')

lawyers_links = links.values.tolist()
#%%
# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path = '/Users/santiagopardo/Documents/WJP/WebScrapping/chromedriver_m1',
                          options         = options)

lawyers_links = [re.sub("\[|\]|'", "", str(element)) for element in lawyers_links]


#%%
# Extracting information from individual links
N = 7382

#lawyers_list = []
for link in lawyers_links[N:9346]:
    driver.get(f"{link}")
    driver.implicitly_wait(2)
    content = driver.page_source
    soup    = BeautifulSoup(content, "lxml")
    
    top_block               = soup.find("div", class_ = "av_top")
    try:
        name                    = top_block.find("h1", class_ = "text-capitalize").text.strip()
    except AttributeError:
        name                    = "NA"
    try:
        registration_date       = top_block.find("p", class_ = "ral_r f16").text.strip() 
    except AttributeError:
        regustation_date        = "NA"

    
    
    spec_block              = soup.find("div", class_ = "av_bot_left left")
    
    try:
        telephone               = spec_block.find("em", string = re.compile("Telefon")).find_parent().text.strip()
        telephone               = re.search("(?<=Telefon:\s).+", telephone).group()
    except AttributeError:
        telephone               = "NA"
        
    try:
        spec                    = spec_block.find("em", string = re.compile("Expertiză")).find_parent().text.strip()
        spec                    = re.search("(?<=Expertiză:\s).+", spec).group()
    except AttributeError:
        spec                    = "NA"

    try:
        email                   = spec_block.find("em", string = re.compile("Adresă email")).find_parent().text.strip()
        email                   = re.search("(?<=Adresă email:\s).+", email).group()
    except AttributeError:
        email                   = "NA"
        
    try:
        web_site                = spec_block.find("em", string = re.compile("Site internet")).find_parent().text.strip()
        web_site                = re.search("(?<=Site internet:\s).+", web_site).group()
    except AttributeError:
        web_site                = "NA"
    
    try:
        firm_name               = spec_block.find("em", string = re.compile("Forma de exercitare")).find_parent().text.strip()
        firm_name               = re.search("(?<=Forma de exercitare:\s).+", firm_name).group()
    except AttributeError:
        firm_name               = "NA"
    
    try:
        
        link_address                = spec_block.find("em", string = re.compile("Forma de exercitare")).find_parent()
        link_address                = link_address.find("a", href = True)
        link_address                = link_address["href"]
        print(link_address)
    
        driver.get(f"https://www.baroul-bucuresti.ro{link_address}")
        driver.implicitly_wait(2)
        content = driver.page_source
        soup_address    = BeautifulSoup(content, "lxml")
    
    except AttributeError:
        address               = "NA"
    
    try:
        address                 = soup_address.find("em", string = re.compile("Sediu")).find_parent().text.strip()
        address                 = re.search("(?<=Sediu:\s).+", address).group()
    except AttributeError:
        address                 = "NA" 
        

    print(address)
    
    plink                       = link

    lawyer = {
        "name"                  : name,
        "registration_date"     : registration_date,
        "telephone"             : telephone,
        "spec"                  : spec,
        "email"                 : email,
        "website"               : web_site,
        "firm_name"             : firm_name,
        "address"               : address
        "URL"                   : plink
        } 
    
    lawyers_list.append(lawyer)
    N = N+1
    print(N)

#%%

master_data = pd.DataFrame(lawyers_list)
master_data = master_data.drop_duplicates()

master_data.to_csv("Rumania_9346.csv", index = False, encoding = "utf-8")
