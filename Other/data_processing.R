library(sf)
library(readxl)
library(tidyverse)

# Loading data: Lawyer Data
master_data.sf <- readRDS("Data/EU_masterData.rds")

# Loading data: Country Info
country_info.df <- read_excel(path = "Data/country_ginfo.xlsx")

# Processing sata at the NUTS level
NUTSdata.df <- master_data.sf %>%
  st_drop_geometry() %>%
  filter(!(country %in% c("Spain"))) %>%
  group_by(NUTS_ID) %>%
  mutate(across(ends_with("law"),
                as.double)) %>%
  summarise(
    NUTS_name = first(NAME_LATN),
    country   = first(CNTR_NAME),
    nlawyers  = n(),
    
    CClaw = sum(CClaw, na.rm = T),
    CJlaw = sum(CJlaw, na.rm = T),
    LLlaw = sum(LLlaw, na.rm = T),
    PHlaw = sum(PHlaw, na.rm = T),
    
    phone_firm_bin = sum(phone_firm_bin, na.rm = T),
    firm_email_bin = sum(firm_email_bin, na.rm = T)
  )

saveRDS(NUTSdata.df, "Data/NUTSdata.rds")

# Processing data at the country level
COUNTRYdata.df <- master_data.sf %>%
  st_drop_geometry() %>%
  filter(!(country %in% c("Spain"))) %>%
  mutate(
    country = case_when(
      country == "Czechrep"   ~ "Czech Republic",
      country == "Spain_new"  ~ "Spain",
      TRUE ~ country),
    across(ends_with("law"),
           as.double)) %>%
  group_by(country) %>%
  summarise(
    nlawyers  = n(),
    
    CClaw = sum(CClaw, na.rm = T),
    CJlaw = sum(CJlaw, na.rm = T),
    LLlaw = sum(LLlaw, na.rm = T),
    PHlaw = sum(PHlaw, na.rm = T),
    
    phone_firm_bin = sum(phone_firm_bin, na.rm = T),
    firm_email_bin = sum(firm_email_bin, na.rm = T)
  ) %>%
  left_join(country_info.df) %>%
  left_join(
    master_data.sf %>%
      st_drop_geometry() %>%
      filter(!(country %in% c("Spain"))) %>%
      filter(is.na(NUTS_ID)) %>%
      mutate(
        country = case_when(
          country == "Czechrep"   ~ "Czech Republic",
          country == "Spain_new"  ~ "Spain",
          TRUE ~ country)
      ) %>%
      group_by(country) %>%
      summarise(umatchedNUTS = n())
  )

saveRDS(COUNTRYdata.df, "Data/COUNTRYdata.rds")

# Processing data for map
MAPdata.sf <- master_data.sf %>%
  st_drop_geometry() %>%
  filter(!(country %in% c("Spain"))) %>%
  select(location, firm_email_bin, NUTS_ID, phone_firm_bin, x, y)

saveRDS(MAPdata.sf, "Data/MAPdata.rds")
