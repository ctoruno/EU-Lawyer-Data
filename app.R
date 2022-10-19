## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Script:            EU Webscrapped Data
##
## Author:            Carlos A. Toruño Paniagua   (ctoruno@worldjusticeproject.org)
##
## Creation date:     May 28th, 2022
##
## This version:      October 19th, 2022
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Required packages + functions and data loading
source("R/global.R")

# Setting up waiting screen
waiting_screen <- tagList(
  spin_dots(),
  h4("Server is busy processing data...")
)

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
#                1.  App UI                                                                                 ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

appUI <- navbarPage(
  "Extracted data of EU lawyers", 
  
  ## 1.1 CSS styling  ==========================================================================================
  # Defining a CSS style format for UI:
  tags$style("
        #filters {
          background-color: #E6F2FA;
          opacity: 0.50;
        }
        #filters:hover{
          opacity: 0.85;
        }
        #plotCountry {
          background-color: #E6F2FA;
          opacity: 0.45;
        }
        #plotCountry:hover{
          opacity: 0.95;
        }
        .checkbox-inline { 
                    margin-left: 10px;
                    margin-right: 10px;
        }
        .checkbox-inline+.checkbox-inline {
                    margin-left: 10px;
                    margin-right: 10px;
        }
               "),
  
  id = "navBar",
  
  ## 1.2 Map tab  ==============================================================================================
  tabPanel("Map Overview", 
           # Setting waiters
           useWaiter(),
           waiterOnBusy(
             html    = waiting_screen,
             color   = "white",
             fadeout = 500),
           
           # Map Layout
           leafletOutput("europeMap", 
                         height = 1000),
           absolutePanel(id        = "filters", 
                         class     = "panel panel-default",
                         top       = 75, 
                         left      = 55, 
                         width     = 250, 
                         fixed     = T,
                         draggable = T, 
                         height    = "auto",
                         awesomeCheckboxGroup(
                           inputId  = "filters",
                           label    = "Show only those individuals for whom we have:", 
                           choices  = c("Phone number", 
                                        "E-mail address"),
                           selected = c("Phone number",
                                        "E-mail address"),
                           inline   = T,
                           status   = "danger"
                         ),
                         p(HTML("<p><strong>Total number of available lawyers:</strong></p>")),
                         textOutput("total_individuals")
           )
  ),
  
  ## 1.3 Country tab  ==========================================================================================
  tabPanel("Data per country",
           
           sidebarLayout(
             sidebarPanel(
               width = 3,
               pickerInput(
                 inputId  = "countrySelection",
                 label    = "Choose a country:", 
                 choices  = COUNTRYdata.df$country,
                 selected = "Netherlands"
               )
             ),
             mainPanel(
               htmlOutput("country.header"),
               br(),
               uiOutput("country.ginfo"),
               h3("Webscrapping results"),
               plotlyOutput("country.results", width = 600),
               h3("Contact Information Gathered"),
               plotlyOutput("country.contact", width = 600),
               h3("Top law specializations reported by individuals"),
               DTOutput("top_specs", width = 600),
               h3("Qualified experts for QRQ"),
               plotlyOutput("country.qualified", width = 500)
             )
           )
  ),
  
  ## 1.4 NUTS tab  ==========================================================================================
  tabPanel("Data per NUTS region",
           sidebarLayout(
             sidebarPanel(
               id    = "nutsPanel",
               width = 3,
               pickerInput(
                 inputId  = "nutsSelection",
                 label    = "Choose a country:", 
                 choices  = COUNTRYdata.df$country,
                 selected = "Netherlands"
               )
             ),
             mainPanel(
               htmlOutput("nuts.header"),
               br(),
               uiOutput("nuts.ginfo"),
               h3("Geographical distribution across NUTS regions"),
               plotlyOutput("NUTSoverview", width = 600),
               plotlyOutput("NUTSdistpie", width = 600),
               h3("Contact Information Gathered"),
               uiOutput("NUTSlist"),
               plotlyOutput("gaugeEMAIL", width = 600),
               plotlyOutput("gaugePHONE", width = 600),
               h3("Summary of results by NUTS region"),
               DTOutput("NUTS_DT", width = 600)
             )
           )
  ),
  
  ## 1.5 Info tab  ==========================================================================================
  tabPanel("Info",
           fluidPage(
             h3("Data Sources"),
             p(paste("For information on the several data sources used in this application,",
                     "please download the following Excel file:")),
             a(href = "data_sources.xlsx", "Data Sources", download = NA, target = "_blank"),
             br(),
             h3("Development:"),
             a(href = "https://github.com/ctoruno", "@ctoruno"),
             h3("Data Webscrapping:"),
             a(href = "https://github.com/ctoruno", "@ctoruno"),
             br(),
             a(href = "https://github.com/jaehee99", "@jaehee"),
             br(),
             a(href = "https://github.com/aspardog", "@aspardog"),
             p("@pablo"),
             br(),
             h3("Code:"),
             p("The code used in this Shiny App is publicly available in the following GitHub Repository:"),
             a(href = "https://github.com/ctoruno/EU-Lawyer-Data", "EU-Lawyer-Data"),
           )
  )
)
  
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
#                2.  App SERVER                                                                             ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
appSERVER <- function(input, output, session) {
  
  # Start pop-up message
  showModal(modalDialog(
    title = "Important message",
    paste("This shiny app is still under development. Therefore, this dashboard is only showing the current",
          "data for all listed countries. Data for France is still under collection.",
          "At the same time, this dashboard is processing the data for almost half a million lawyers.",
          "Some listed countries, like France and Italy, might take a few seconds to load.", 
          "We are working on improving the efficiency of the server estimations"),
    easyClose = TRUE
  ))
  
  
  ## 2.1 Map tab  ==============================================================================================
  
  # Creating master data frame
  data4map.rct <- reactive({

    if (sum(c("Phone number", "E-mail address") %in% input$filters) == 2) {
      base_data.sf <- MAPdata.sf %>%
        filter(phone_firm_bin == 1 & firm_email_bin == 1)
    } else if ("Phone number" %in% input$filters) {
      base_data.sf <- MAPdata.sf %>%
        filter(phone_firm_bin == 1)
    } else if ("E-mail address" %in% input$filters) {
      base_data.sf <- MAPdata.sf %>%
        filter(firm_email_bin == 1)
    } else {
      base_data.sf <- MAPdata.sf
    }
        
    # Retrieving coordinates
    base_data.sf <- base_data.sf %>%
      rename(longitude = x,
             latitude  = y) %>%
      mutate(across(c(longitude, latitude),
                    as.double))
    
    # Adding coordinates
    location_data.sf <- base_data.sf %>%
      group_by(location) %>%
      summarise(N         = n(),
                latitude  = first(latitude),
                longitude = first(longitude)) %>%
      mutate(label4map = paste("<p><strong>", location, "</strong><br/>",
                               "Number of lawyers: ", N, "</p>"))
    
    return(list(base_data.sf, location_data.sf))
  })
  
  # Rendering total number of individuals
  output$total_individuals <- renderText({
    format(nrow(data4map.rct()[[1]]),
           big.mark = ",")
  })
  
  # Rendering leaflet map 
  output$europeMap <- renderLeaflet({
    
    leaflet() %>% 
      addProviderTiles(providers$CartoDB.Voyager) %>%
      setView(lng = 9.183333, 
              lat = 40.783333, 
              zoom = 5) %>%
      # addPolygons(data    = NUTS.sf,
      #             color   = "#F7E9C1",
      #             opacity = 0.95,
      #             stroke  = F) %>%
      addCircleMarkers(data         = data4map.rct()[[2]],
                       lng          = ~longitude,
                       lat          = ~latitude,
                       radius       = ~(N)^(1/3.5),
                       color        = "#00A08A",
                       fillOpacity  = 0.1,
                       label        = lapply(data4map.rct()[[2]]$label4map, HTML),
                       labelOptions = labelOptions(style = list("font-weight" = "normal", 
                                                                padding = "3px 8px", 
                                                                "color" = "#00A08A"),
                                                   textsize  = "15px", 
                                                   direction = "auto"))
  })
  
  ## 2.2 Country tab  ==========================================================================================
  
  # Defining data for Country Panel
  data4countryPanel.rct <- reactive({
     COUNTRYdata.df %>%
      filter(country == input$countrySelection)
  })
  
  # Rendering general info and header
  output$country.header <- renderText({
    c(
      '<div style="display:inline-block;vertical-align:top;">',
      '<img src="', data4countryPanel.rct() %>% pull(flag), '" alt="img" width="100" height="75"/>',
      '</div>
          <div style="display:inline-block; margin: 10px;">
          <h3>', input$countrySelection,'</h3>
      </div>'
    )
  })
  
  output$country.ginfo <- renderUI({
    tagList(
      tags$div(
        tags$ul(
          tags$li(strong("Population (2021):"), 
                  format(data4countryPanel.rct() %>% 
                           pull(population), 
                         big.mark = ",")),
          br(),
          tags$li(strong("Official languages:"), 
                  data4countryPanel.rct() %>% 
                    pull(languages)),
          br(),
          tags$li(strong("Lawyers registered at the bar associations (last estimation):"), 
                  format(data4countryPanel.rct() %>% 
                           pull(eurostat_est), 
                         big.mark = ","))
        )
      )
    )
  })
  
  # Rendering Webscrapping Results
  output$country.results <- renderPlotly({
    toPlotly <- COUNTRYresults_panel.fn(data = data4countryPanel.rct())
    ggplotly(toPlotly, tooltip = NULL)
  })
  
  # Rendering Contact Information
  output$country.contact <- renderPlotly({
    COUNTRYcontact_panel.fn(data = data4countryPanel.rct())
  })
  
  # Rendering Top Specializations
  output$top_specs <- renderDT({
    datatable(COUNTRYspecializations.fn(selection = input$countrySelection),
              options = list(dom = "t",
                             language = list(emptyTable = "No specialization data for this country")))
  })
  
  # Rendering qualified individuals plotly
  output$country.qualified <- renderPlotly({
    toPlotly <- COUNTRYqualified_panel.fn(data = data4countryPanel.rct())
    ggplotly(toPlotly, tooltip = NULL)
  })
  
  ## 2.2 NUTS tab  ==========================================================================================
  
  # Defining data for NUTS Panel
  data4nutsPanel.rct <- reactive({
    NUTSdata.df %>%
      filter(country == input$nutsSelection)
  })
  
  # Rendering general info and header
  output$nuts.header <- renderText({
    c(
      '<div style="display:inline-block;vertical-align:top;">',
      '<img src="', COUNTRYdata.df %>% filter(country == input$nutsSelection) %>% pull(flag), 
      '" alt="img" width="100" height="75"/>',
      '</div>
          <div style="display:inline-block; margin: 10px;">
          <h3>', input$nutsSelection,'</h3>
      </div>'
    )
  })
  
  output$nuts.ginfo <- renderUI({
    tagList(
      tags$div(
        tags$ul(
          tags$li(strong("Population (2021):"), 
                  format(COUNTRYdata.df %>% 
                           filter(country == input$nutsSelection) %>% 
                           pull(population), 
                         big.mark = ",")),
          br(),
          tags$li(strong("Official languages:"), 
                  COUNTRYdata.df %>% 
                    filter(country == input$nutsSelection) %>% 
                    pull(languages)),
          br(),
          tags$li(strong("Lawyers registered at the bar associations (last estimation):"), 
                  format(COUNTRYdata.df %>% 
                           filter(country == input$nutsSelection) %>% 
                           pull(eurostat_est), 
                         big.mark = ",")),
          br(),
          tags$li(strong("Lawyers successfully geocoded to a NUTS region::"), 
                  format(NUTSdata.df %>% 
                           filter(country == input$nutsSelection) %>% 
                           group_by(country) %>% 
                           summarise(sum = sum(nlawyers, 
                                               na.rm = T)) %>% 
                           pull(sum), 
                         big.mark = ",")),
          br(),
          tags$li(strong("Lawyers residing in an unknown region:"), 
                  format(COUNTRYdata.df %>%
                           filter(country == input$nutsSelection) %>% 
                           pull(umatchedNUTS), 
                         big.mark = ","))
        )
      )
    )
  })
  
  # Rendering overview map
  output$NUTSoverview <- renderPlotly({
    toplotly <- NUTSmap.fn(selection = input$nutsSelection)
    ggplotly(toplotly)
  })
  
  # Rendering distribution pie
  output$NUTSdistpie <- renderPlotly({
    NUTSdistribution.fn(selection = input$nutsSelection)
  })
  
  # Rendering UI for NUTS list picker
  output$NUTSlist <- renderUI({
    pickerInput(
      inputId  = "specificNUTS",
      label    = "Choose a region:", 
      choices  = NUTSdata.df %>% 
                  filter(country == input$nutsSelection) %>% 
                  pull(NUTS_name)
    )
  })
  
  # Rendering Gauge EMAIL
  output$gaugeEMAIL <- renderPlotly({
    gaugeChart.fn(selectionC = input$nutsSelection, 
                  selectionN = input$specificNUTS, 
                  value      = "email")
  })
  
  # Rendering Gauge PHONE
  output$gaugePHONE <- renderPlotly({
    gaugeChart.fn(selectionC = input$nutsSelection, 
                  selectionN = input$specificNUTS, 
                  value      = "phone")
  })
  
  # Rendering DT summary table
  output$NUTS_DT <- renderDT({
    toDT <- NUTSdt.fn(selection = input$nutsSelection)
    datatable(toDT)
  })
  
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
#                3.  App DEPLOYMENT                                                                         ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Run the application 
shinyApp(ui = appUI, server = appSERVER)

# library(rsconnect)
# deployApp()
