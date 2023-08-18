#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 2022

@author: carlostorunopaniagua
"""

# Libraries needed
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

from selenium import webdriver

#%%

#%%

# Setting up a Selenium webdriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path = '/Users/carlostorunopaniagua/Documents/GitHub/chromedriver',
                          options         = options)

#%%

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

#%%

root_url = "https://dsk.gr/member_list/"

# Getting website in the driver
driver.get(root_url)

# Fetching/Parsening
content = driver.page_source


soup    = BeautifulSoup(content)



#%%

# Creating an empty list to store results
lawyers_list = []

# Fetching/Paresening
root_url = "https://www.dskaterinis.gr/lawyers/"
response = requests.get(root_url, headers = headers)
soup     = BeautifulSoup(response.text, "lxml")