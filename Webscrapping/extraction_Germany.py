#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:19:34 2022

@author: carlostorunopaniagua
"""

#%%

# Libraries needed
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from io import BytesIO
import PyPDF2
import re

# %%

# Defining parameters
start_link = 52250
end_link   = 58648
coder      = "Santiago"
batch      = 6

# Defining headers
agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ",
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
         "96.0.4664.110 Safari/537.36"]
headers = {
    "User-Agent": "".join(agent)
}

#%%

# DEFINING FUNCTIONS

# Defining a link extraction function
def fetch_links(page):

    # Define the root URL to scrap:
    root_url = f"https://anwaltauskunft.de/anwaltssuche?page={page}"

     # Fetching/parsening
    root_response = requests.get(root_url, 
                                 headers = headers)
    root_soup     = BeautifulSoup(root_response.text, "lxml")
    time.sleep(2)

    # Extracting links
    card_body = root_soup.find("div", class_ = "card-body p-0")
    results = [card.find("a").get("href") for card 
                in card_body.findAll("div", class_ = "lawyer lawyer-list")]

    return results

# Defining a function to extract the information from a website
def html_extraction(lawyer_extension):
    
    # Define the root URL to scrap:
    base_url = f"https://anwaltauskunft.de/{lawyer_extension}"

    # Fetching/parsening
    base_response = requests.get(base_url, 
                                 headers = headers)
    base_soup     = BeautifulSoup(base_response.text, "lxml")
    time.sleep(2)

    # Extracting info from the website
    name    = base_soup.find("div", class_ = "h1 name").text.strip()
    
    try :
        address = base_soup.find("address").text.strip()
        address = re.sub("\n", ", ", address)
    except AttributeError:
        address = "NA"

    try:
        specs   = base_soup.find("div", class_ = "lawyer-sections").find("h6")
        specs   = specs.find_next_sibling("div").text.strip()
        specs   = re.sub("\n|\n\n", ", ", specs)
    except AttributeError:
        specs   = "NA"
    
    try:
        languages = base_soup.find("div", class_ = "lawyer-languages").find("h6")
        languages = languages.find_next_sibling("ul").text.strip()
    except AttributeError:
        languages = "NA"

    # Getting PDF URL
    header  = base_soup.find("div", class_ = "lawyer-detail-head m-0").select_one("div > div:nth-child(1)")
    pdf_btn = header.find("ul").select_one("ul > li:nth-child(2)")
    pdf_ext = pdf_btn.find("a").get("href")

    # Defining dictionary entry
    dct = {
        "name"               : name,
        "address"            : address,
        "specializations"    : specs,
        "languages"          : languages,
        "PDF"                : pdf_ext,
        "URL"                : base_url
        }

    return dct

# Defining a function to extract the information from the online PDF
# IMPORTANT!! READ THE FOLLOWING SO POST: https://stackoverflow.com/a/64997181

def pdf_extraction(pdf_extension):

    # Define the pead URL to read the document
    pdf_url = f"https://anwaltauskunft.de/{pdf_extension}"

    # Fetching/parsening
    pdf_response = requests.get(pdf_url, 
                                headers = headers)
    pdf_raw      = pdf_response.content
    time.sleep(2)

    # Reading document
    with BytesIO(pdf_raw) as data:
        read_pdf = PyPDF2.PdfFileReader(data)
        pdfTEXT  = read_pdf.getPage(0).extractText()
        pdfTEXT  = re.sub("\n(?=[A-Z]{1})", "%%", pdfTEXT)
        pdfTEXT  = re.sub("\n", "", pdfTEXT)

    # Extracting information
    try:
        email = re.findall("(?<=Mail:).+?(?=%%)", pdfTEXT)
        email = " <OR> ".join(email)
    except AttributeError:
        email = "NA"

    try:
        phone = re.findall("(?<=Tel.:).+?(?=%%)", pdfTEXT)
        phone = " <OR> ".join(phone)
    except AttributeError:
        phone = "NA"
    
    try:
        web   = re.findall("(?<=Web:).+?(?=%%)", pdfTEXT)
        web   = " <OR> ".join(web)
    except AttributeError:
        web   = "NA"
    
    # Defining dictionary entry
    dct = {
        "phone"              : phone,
        "email"              : email,
        "web"                : web
        }

    return dct

#%%

# Reading links CSV
lawyers_links = pd.read_csv("Germany_links.csv")["0"].tolist()

# Creating an empty list to store results
#lawyers_list = []

#%%

# Setting up a counter
N = start_link

# Looping across links to retrieve information
for link in lawyers_links[start_link:end_link+1]:

    print("Currently extracting information from link no. " + str(N))

    # Applying functions to retrieve information
    try:
        html_info = html_extraction(link)
        pdf_info  = pdf_extraction(html_info["PDF"])

        # Joining dictionaries
        full_info = {**html_info, **pdf_info}

        # Appending to main list
        lawyers_list.append(full_info)

    except AttributeError:
        print("Not possible to scrap") 

    # Updating counter
    N = N + 1

#%% 

# Saving data into a dataframe    
master_data = pd.DataFrame(lawyers_list).drop_duplicates()
master_data.to_csv(f"Germany_{coder}_batch{batch}.csv", 
                   index    = False, 
                   encoding = "utf-8") 


