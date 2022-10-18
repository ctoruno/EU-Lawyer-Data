## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Script:            EU Lawyer Data - Country Selection Module
##
## Author:            Carlos A. Toruño Paniagua   (ctoruno@worldjusticeproject.org)
##
## Dependencies:      World Justice Project
##
## Creation date:     October 13th, 2022
##
## This version:      October 14th, 2022
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Outline:                                                                                                 ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                1.  Country Selection UI                                                                  ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

countrySelection_input <- function(id){
  ns <- NS(id)
  tagList(
    div(
      id = ns("picker"),
      pickerInput(
        inputId  = ns("selected_country"),
        label    = "Choose a country:", 
        choices  = COUNTRYdata.df$country,
        selected = "Netherlands"
      )
    )
  )
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                1.  Country Selection SERVER                                                              ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

countrySelection_server <- function(id, glob){
  moduleServer(
    id,
    function(input, output, session){
      
      reactive({
        glob$selected_country <- input$selected_country
      }) %>% 
        bindEvent(input$selected_country)
    }
  )
}