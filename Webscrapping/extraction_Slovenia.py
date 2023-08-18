#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:46:00 2022

@author: carlostorunopaniagua
"""
#%%

# Libraries needed
import pandas as pd
from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
import re
import json
# import lxml


# Header definition
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

url = "https://www.odv-zb.si/odvetniska-zbornica/imenik/imenik-odvetnikov/"

#%%

# Retrieving source code:
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

#%%

# Data is embeddded as JSON code within source code.
# Defining a regular expression to retrieve data:
pattern = "var dataSet = (.+?);\n"

# Data is located within a <script> tag.
# Retrieving all script tags info and using regular expressions to select data:
blocks = []
for scraps in soup.findAll("script"):
    scrappy  = scraps.text
    raw_data = re.findall(pattern, scrappy, re.S)
    blocks.append(raw_data)

# Selecting the element, from all the script tags, that has the data:
index = [idx for idx, element in enumerate(blocks) if len(element) > 0]
data_str = blocks[index[0]]

# Converting to JSON object:
if data_str:
    data_json = json.loads(data_str[0]) # we need to remove the ";" delimiter.

# Converting to Pandas Data Frame:
data_frame = pd.DataFrame.from_dict(data_json)
data_frame = data_frame.rename(columns = {"Ime":"name",
                                          "Priimek":"surname",
                                          "Zaposlitev":"employment",
                                          "Naslov":"address",
                                          "Kraj":"city",
                                          "Telefon":"telephone",
                                          "Splet":"web_contact",
                                          "Območni zbor":"regional_assembly",
                                          "Jezik":"languages",
                                          "Tuji":"foreign",
                                          "Področje prava":"field",
                                          "Naziv":"title"})

# Saving data as a CSV file:
# data_frame.to_csv("Slovenia_1895_example.csv", index = False)
