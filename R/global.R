# Load libraries
library(shiny)
library(shinyWidgets)
library(leaflet)
library(plotly)
library(sf)
library(DT)
library(terra)
library(tidyverse)

# Loading data
MAPdata.sf      <- readRDS("Data/MAPdata.rds")
COUNTRYdata.df  <- readRDS("Data/COUNTRYdata.rds")
NUTSdata.df     <- readRDS("Data/NUTSdata.rds")

# Source scripts
source("R/functions.R")

