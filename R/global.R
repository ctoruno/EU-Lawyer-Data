# Load libraries
library(shiny)
library(shinyWidgets)
library(leaflet)
library(plotly)
library(sf)
library(DT)
library(terra)
library(waiter)
library(tidyverse)

# Loading data
MAPdata.sf      <- readRDS("Data/MAPdata.rds")
COUNTRYdata.df  <- readRDS("Data/COUNTRYdata.rds")
NUTSdata.df     <- readRDS("Data/NUTSdata.rds")

# Loading NUTS shapefile
NUTS.sf <- st_read("Data/NUTS/EU SUBNATIONAL WJP.shp")

# Loading top specializations per country
topSpecs.ls <- readRDS("Data/topSpecs.rds")

# Source scripts
source("R/functions.R")

# NUTS color palette - MAP
nutsPalette <- c("#F9ECE1", "#F0D4BB", "#F3DCC8", "#ECCBAE", "#DFB693", "#DEAA8B",
                 "#DC9E82", "#C98C75", "#B57967", "#A16659", "#975D52", "#8D534B",
                 "#834A45", "#79413E", "#652E30", "#5B2529", "#511B22", "#47121B")

# Color Palettes - NUTS PIE
distpie_5  <- c("#3F3F37", "#D6D6B1", "#494331", "#878472", "#DB8A74")

distpie_8  <- c("#F1F2EB", "#D8DAD3", "#A4C2A5", "#7D9276", 
                "#566246", "#505647", "#4A4A48", "#343432")

distpie_18 <- c("#628395", "#6F858F", "#7C8688", "#898882", "#96897B", "#B99B73",
                "#CAA46F", "#DBAD6A", "#D5A365", "#CF995F", "#D0A767", "#D0B16D",
                "#D0BB72", "#D0CE7C", "#ACAE71", "#878E66", "#636E5B", "#3E4E50")