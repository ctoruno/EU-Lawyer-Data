#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 07:14:46 2022

@author: carlostorunopaniagua
"""

#%%

import pandas as pd
import requests

#%%

# Defining headers
agent = ["Carlos Toruno using Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]

# API definition
headers = {
    "User-Agent"       : "".join(agent),
    "X-Requested-With" : "XMLHttpRequest"
}

# URL
url = "https://findanattorney.fi/api/loyda?lang=fi&"

# Retrieving and saving data
response = requests.get(url)
data     = response.json()
master_data = pd.DataFrame.from_dict(data)
master_data.to_csv("Finland_2232.csv", index = False, encoding = "utf-8")

