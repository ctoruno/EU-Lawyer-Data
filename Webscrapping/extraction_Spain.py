#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:49:34 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import time
import requests
import re
import math
import pandas as pd
from bs4 import BeautifulSoup

#%%

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]

# API definition
headers = {
    "User-Agent"       : "".join(agent),
}

# Defining a decoding class:
# See: https://stackoverflow.com/questions/36911296/scraping-of-protected-email
def deCFEmail(fp):
        try:
            r = int(fp[:2],16)
            email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
            return email
        except (ValueError):
            pass

#%%

root_url = "https://iurisnow.com/es/localizaciones/"

response  = requests.get(root_url)
root_soup = BeautifulSoup(response.text, "lxml")  

cities = []
cities_soup   = root_soup.find("section", {"id" : "ciudades"}).select(".ciudad")
for city in cities_soup:
    location  = re.search("(?<=Abogados\s).+", city.find("h2").text).group()
    city_url  = city.find("a", href = True)["href"]     
    city_info = (location, city_url)
    cities.append(city_info)
    
lawyers_list = []

N1 = 44
N2 = 46


#%%

for city, url in cities[N1:N2+1]:
    print("<<<<<<<<>>>>>>>>")
    
    # Fetching HTML code
    response  = requests.get(url)
    city_soup = BeautifulSoup(response.text, "lxml") 
    time.sleep(2)

    # How many lawyers and how many pages do we need in current location?
    try:
        nlawyers  = re.search("(?<=Tenemos\s).+(?=\sAbogados)", city_soup.select_one(".total").text).group()
    except AttributeError:
        nlawyers  = re.search("(?<=Tenemos\s).+(?=\sLos)", city_soup.select_one(".total").text).group()
        
    npages    = math.ceil(int(nlawyers)/30)
    
    # Looping across pages
    for page in range(1, npages+1):
        
        print("Currently extracting info from page: " + str(page) + ", " + city)   
        # Extracting city URL from tupple
        current_URL = url + f"page/{page}/"
        
        if page > 1:
            # Fetching HTML code
            response  = requests.get(current_URL)
            city_soup = BeautifulSoup(response.text, "lxml") 
            time.sleep(2)

        # Extracting lawyer info
        for person in city_soup.find("section", id = "abogados").findAll("div", class_ = "content"):
            name  = person.find("h3").text.strip()
            try:
                plink = person.find("h3").find("a", href = True)["href"]
            except TypeError:
                plink = person.find("h3").find("span").get("onclick")
                plink = re.search("(?<=href\=').+(?=')", plink).group()
                            
            try:
                budget = person.find("div", class_ = "presupuesto").find("a", href = True)["href"]
            except TypeError:
                budget = "None"
            except AttributeError:
                budget = "None"
            
            match      = re.search("email", budget)
            if match:
                email  = re.search("(?<=email-protection#).+", budget).group()
                email  = deCFEmail(email)
            else:
                email  = "None"
            
            match      = re.search("tel", budget)   
            if match:
                phone  = re.search("(?<=tel:).+", budget).group()
            else:
                phone  = "None"
            
            # Defining dictionary entry
            lawyer = {
                "name"               : name,
                "URL"                : plink,
                "district"           : city,
                "phone"              : phone,
                "email"              : email
                } 
            
            # Appending to main list
            lawyers_list.append(lawyer)

#%%

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list)
master_data.to_csv("Spain_172155.csv", index = False, encoding = "utf-8")
    
