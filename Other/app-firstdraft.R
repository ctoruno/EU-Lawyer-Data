## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Script:            EU Webscrapped Data
##
## Author:            Carlos A. Toruño Paniagua   (catoruno@worldjusticeproject.org)
##
## Creation date:     October 13th, 2022
##
## This version:      October 13th, 2022
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Required packages + functions and data loading
source("R/global.R")

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
                           label    = "Filter by:", 
                           choices  = c("Has home address", 
                                        "Has phone number", 
                                        "Has email address"),
                           selected = c("Has phone number",
                                        "Has email address"),
                           inline   = T,
                           status   = "danger"
                         ),
                         p(HTML("<p><strong>Total number of available lawyers:</strong></p>")),
                         textOutput("total_individuals")
           ),
           absolutePanel(id        = "plotCountry", 
                         class     = "panel panel-default",
                         top       = 500, 
                         right     = 25, 
                         width     = 200, 
                         fixed     = T,
                         draggable = T, 
                         height    = "auto",
                         strong("No. of lawyers per country"),
                         plotlyOutput("totalCountry",
                                      height = "150px")
           )
  ),
  
  ## 1.3 Country tab  ==========================================================================================
  tabPanel("Data per country",
           sidebarLayout(
             sidebarPanel(
               width = 3,
               pickerInput(
                 inputId = "countrySelection",
                 label   = "Choose a country:", 
                 choices = names(country_data),
                 selected = "Netherlands"
               )
             ),
             mainPanel(
               htmlOutput("header"),
               br(),
               uiOutput("general_info"),
               h3("Webscrapping results"),
               plotlyOutput("results", width = 600),
               h3("Top law specializations reported by individuals"),
               plotlyOutput("top_specs", width = 600),
               h3("Qualified experts for QRQ"),
               plotlyOutput("qualified", width = 500),
               h3("Number of qualified experts per questionnaire"),
               plotlyOutput("QRQ", width = 600),
               h3("Top registered law firms within extracted data"),
               DTOutput("topFirms", width = 600)
             )
           )
  )
)
  
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
#                2.  App SERVER                                                                             ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
appSERVER <- function(input, output, session) {
  
  ## 2.1 Data processing  ======================================================================================
  
  # Creating master data frame
  master_data.rve <- reactive({
    
    base_data.sf <- imap(country_data,
                         function(CNT, CNTname){
                           
                           CNT.df <- CNT %>%
                             select(location, 
                                    has_address, 
                                    firm_email_bin, 
                                    phone_firm_bin,
                                    CClaw, CJlaw, LLlaw, PHlaw) %>%
                             mutate(country = CNTname)
                           
                         }) %>% bind_rows()

    if (sum(c("Has home address", "Has phone number", "Has email address")  %in% input$filters) == 3) {
      base_data.sf <- base_data.sf %>%
        filter(has_address    == 1 | phone_firm_bin == 1 | firm_email_bin == 1)
    } else if (sum(c("Has home address", "Has phone number")   %in% input$filters) == 2) {
      base_data.sf <- base_data.sf %>%
        filter(has_address    == 1 | phone_firm_bin == 1)
    } else if (sum(c("Has phone number", "Has email address")  %in% input$filters) == 2) {
      base_data.sf <- base_data.sf %>%
        filter(phone_firm_bin == 1 | firm_email_bin == 1)
    } else if ("Has home address"    %in% input$filters) {
      base_data.sf <- base_data.sf %>%
        filter(has_address    == 1)
    } else if ("Has phone number"    %in% input$filters) {
      base_data.sf <- base_data.sf %>%
        filter(phone_firm_bin == 1)
    } else if ("Has email address"   %in% input$filters) {
      base_data.sf <- base_data.sf %>%
        filter(firm_email_bin == 1)
    }
        
    # Retrieving coordinates
    coordinates            <- st_coordinates(base_data.sf)
    base_data.sf$longitude <- coordinates[,1]
    base_data.sf$latitude  <- coordinates[,2]
    
    # Adding coordinates
    location_data.sf <- base_data.sf %>%
      st_drop_geometry() %>%
      group_by(location) %>%
      summarise(N         = n(),
                latitude  = first(latitude),
                longitude = first(longitude)) %>%
      mutate(label4map = paste("<p><strong>", location, "</strong><br/>",
                               "Number of lawyers: ", N, "</p>"))
    
    return(list(base_data.sf, location_data.sf))
  })
  
  ## 2.2 Map tab  ==============================================================================================
  
  # Rendering total number of individuals
  output$total_individuals <- renderText({
    format(nrow(master_data.rve()[[1]]),
           big.mark = ",")
  })
  
  # Rendering per country totals
  output$totalCountry <- renderPlotly({
    ggplot <- ggplot(master_data.rve()[[1]] %>% 
                       st_drop_geometry() %>%
                       group_by(country) %>%
                       count() %>%
                       rename(Country     = country,
                              Individuals = n),
                     aes(x = reorder(Country, Individuals),
                         y = Individuals)) +
      geom_bar(fill = "#9cba8f",
               stat = "identity") +
      # geom_text(aes(y     = n/2,
      #               label = format(n,
      #                              big.mark = ",")),
      #           color     = "white",
      #           fontface  = "bold") +
      coord_flip() +
      theme_bw() +
      theme(
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        axis.text.x  = element_blank(),
        axis.ticks   = element_blank(),
        panel.grid   = element_blank()
      )
    
    ggplotly(ggplot, tooltip = "Individuals") %>%
      config(displayModeBar = F)
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
      addCircleMarkers(data         = master_data.rve()[[2]],
                       lng          = ~longitude,
                       lat          = ~latitude,
                       radius       = ~(N)^(1/3.5),
                       color        = "#00A08A",
                       fillOpacity  = 0.1,
                       label        = lapply(master_data.rve()[[2]]$label4map, HTML),
                       labelOptions = labelOptions(style = list("font-weight" = "normal", 
                                                                padding = "3px 8px", 
                                                                "color" = "#00A08A"),
                                                   textsize  = "15px", 
                                                   direction = "auto"))
  })
  
  ## 2.3 Country tab  ==========================================================================================
  
  # Defining data for Country Panel
  data4countryPanel <- reactive({
    country_data[[input$countrySelection]]
  })
  
  # Filtering general info for each country
  ginfo.rct <- reactive({
    ginfo.df %>%
      filter(country == input$countrySelection) 
  })
  
  # Rendering general info panel
  output$header <- renderText({
    c(
      '<div style="display:inline-block;vertical-align:top;">',
        '<img src="', ginfo.rct() %>% pull(flag), '" alt="img" width="100" height="75"/>',
      '</div>
          <div style="display:inline-block; margin: 10px;">
          <h3>', input$countrySelection,'</h3>
      </div>'
    )
  })

  output$general_info <- renderUI({
    tagList(
      tags$div(
        tags$ul(
          tags$li(strong("Population (2021):"), 
                  format(ginfo.rct() %>% pull(population), big.mark = ",")),
          br(),
          tags$li(strong("Official languages:"), 
                  ginfo.rct() %>% pull(languages)),
          br(),
          tags$li(strong("Lawyers registered at the bar associations (last estimation):"), 
                  format(ginfo.rct() %>% pull(nlawyers), big.mark = ","))
        )
      )
    )
  })
  
  # Rendering Webscrapping Results
  output$results <- renderPlotly({
    toPlotly <- results_panel.fn(data = data4countryPanel(),
                                 reg  = ginfo.rct() %>% pull(nlawyers))
    ggplotly(toPlotly, tooltip = NULL)
  })
  
  # Rendering Top Specializations
  output$top_specs <- renderPlotly({
    toPlotly <- topspecs_panel.fn(data = data4countryPanel())
    ggplotly(toPlotly)
  })
  
  # Qualified experts ggplots
  expertsPlots <- reactive({
    specialization_panel.fn(data = data4countryPanel())
  })
  
  # Rendering qualified individuals plotly
  output$qualified <- renderPlotly({
    ggplotly(expertsPlots()[[1]], tooltip = NULL)
  })
  
  # Rendering qualified individuals per questionnaire
  output$QRQ <- renderPlotly({
    ggplotly(expertsPlots()[[2]], tooltip = NULL)
  })
  
  # Rendering top firms DT
  output$topFirms <- renderDT({
    datatable(top_firms_panel.fn(data = data4countryPanel()),
              options = list(dom = "t",
                             language = list(emptyTable = "No firm data for this country")))
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
