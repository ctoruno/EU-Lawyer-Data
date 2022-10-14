# Load libraries
library(shiny)
library(shinyWidgets)
library(leaflet)
library(plotly)
library(readxl)
library(sf)
library(DT)
library(terra)
library(ggtext)
library(tidyverse)

# Loading countries datasets
country_files.ls <- list.files("Data")[str_detect(list.files("Data"), "\\.rds")]

country_data <- lapply(country_files.ls, 
                     function(country){
                       path2file <- paste0("Data/", country)
                       countryData <- readRDS(path2file)
                       
                       firm_bol <- "firm_name" %in% names(countryData)
                       if (firm_bol == F){
                         countryData <- countryData %>%
                           mutate(firm_name = NA_character_)
                       }
                       
                       spec_bol <- "spec_english" %in% names(countryData)
                       if (spec_bol == F){
                         countryData <- countryData %>%
                           mutate(spec_english_1 = "Unknown")
                       }
                       
                       return(countryData)
                     })

names(country_data) <- str_to_title(str_replace(country_files.ls, "\\.rds", ""))

# Load NUTS shapefile
NUTS.sf <- st_read("Data/NUTS_mapping/NUTS_RG_20M_2021_4326.shp") %>%
  filter(NUTS_ID != "FRY")

# load general info data frame
ginfo.df <- read_excel("Data/country_ginfo.xlsx")

# Source scripts
source("R/functions.R")

