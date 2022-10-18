## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Script:            EU Lawyer Data - Functions
##
## Author:            Carlos A. Toruño Paniagua   (ctoruno@worldjusticeproject.org)
##
## Dependencies:      World Justice Project
##
## Creation date:     May 28th, 2022
##
## This version:      October 17th, 2022
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Outline:                                                                                                 ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Presetting                                                                                ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Defining a WJP theme function
WJP_theme <- function(){
  theme(panel.background   = element_rect(fill = "white", 
                                          size = 2),
        panel.grid.minor   = element_blank(),
        axis.title.y       = element_blank(),
        axis.title.x       = element_blank(),
        axis.text.y        = element_text(family = "Fira Sans", 
                                          face   = "bold", 
                                          size   = 8, 
                                          color  = "Black"),
        axis.text.x        = element_text(family = "Fira Sans", 
                                   face   = "bold", 
                                   size   = 8, 
                                   color  = "Black"),
        axis.ticks         = element_blank(),
        axis.line.x.bottom = element_line(size = 1.75, 
                                          colour = "black", 
                                          linetype = "solid")
  )
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Webscrapping General Results (COUNTRY PANEL)                                              ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

COUNTRYresults_panel.fn <- function(data) {
  
  # Preparing data for plot
  data2plot <- data %>%
    select(`Extracted\nLawyers` = nlawyers, 
           `EUROSTAT\nEstimation` = eurostat_est) %>%
    pivot_longer(everything(),
                 values_to = "No. of Lawyers",
                 names_to  = "Category")
  
  # Make the plot
  ggplot(data  = data2plot, 
         aes(x = Category, 
             y = `No. of Lawyers`)) +
    geom_col(fill  = "#949C81",
             width = 0.75) +
    geom_text(aes(y     = `No. of Lawyers`/2,
                  label = format(`No. of Lawyers`, 
                                 big.mark = ",")),
              color     = "white",
              size      = 4,
              fontface  = "bold") +
    scale_y_continuous(expand = c(0,0)) +
    WJP_theme() +
    theme(panel.grid.major.y = element_line(size     = 0.5, 
                                            colour   = "grey93", 
                                            linetype = "solid"))
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Contact Information Results (COUNTRY PANEL)                                              ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

COUNTRYcontact_panel.fn <- function(data) {
  
  # Preparing data for pie charts
  emailDATA <- data.frame("Categorie" = c("With E-mail Address", 
                                          "Without E-mail Address"),
                          "Value"     = c(data %>% pull(firm_email_bin), 
                                          (data %>% pull(nlawyers)) - (data %>% pull(firm_email_bin)))) 
  
  phoneDATA <- data.frame("Categorie" = c("With Phone Number", 
                                          "Without Phone Number"),
                          "Value"     = c(data %>% pull(phone_firm_bin), 
                                          (data %>% pull(nlawyers)) - (data %>% pull(phone_firm_bin))))
  
  # Making the plotly
  plot_ly() %>%
    add_pie(data         = emailDATA,
            name         = "E-mail",
            labels       = ~Categorie, 
            values       = ~Value, 
            type         = "pie",
            textposition = "inside",
            textinfo     = "label+percent",
            hoverinfo    = "text",
            text         = ~paste("Total Number of Lawyers:<br>",
                                  format(Value, 
                                         big.mark = ",")),
            textfont     = list(family = "Fira Sans"),
            marker       = list(colors = c("#2B4162", "#DC9E82"),
                                line   = list(color = "#FFFFFF", 
                                              width = 1)),
            showlegend   = F,
            domain       = list(row = 0, column = 0)) %>%
    add_pie(data         = phoneDATA,
            name         = "Phone",
            labels       = ~Categorie, 
            values       = ~Value, 
            type         = "pie",
            textposition = "inside",
            textinfo     = "label+percent",
            hoverinfo    = "text",
            text         = ~paste("Total Number of Lawyers:<br>",
                                  format(Value, 
                                         big.mark = ",")),
            textfont     = list(family = "Fira Sans"),
            marker       = list(colors = c("#2B4162", "#DC9E82"),
                                line   = list(color = "#FFFFFF", 
                                              width = 1)),
            showlegend   = F,
            domain       = list(row = 0, column = 1)) %>%
    layout(grid  = list(rows    = 1, 
                        columns = 2),
           xaxis = list(showgrid       = F, 
                        zeroline       = F, 
                        showticklabels = F),
           yaxis = list(showgrid       = F, 
                        zeroline       = F, 
                        showticklabels = F),
           annotations = list(
             list(
               x = 0.225, 
               y = 0.95, 
               font = list(size = 16), 
               text = "How many can we contact<br>through E-mail?", 
               xref = "paper", 
               yref = "paper", 
               xanchor = "center", 
               yanchor = "bottom", 
               showarrow = FALSE
             ), 
             list(
               x = 0.775, 
               y = 0.95, 
               font = list(size = 16), 
               text = "How many can we contact<br>through Phone?", 
               xref = "paper", 
               yref = "paper", 
               xanchor = "center", 
               yanchor = "bottom", 
               showarrow = FALSE
             )
           )
    ) 
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Qualified Experts (COUNTRY PANEL)                                                         ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

COUNTRYqualified_panel.fn <- function(data) {
  
  data2plot <- data %>%
    select(ends_with("law")) %>%
    pivot_longer(everything(),
                 names_to  = "Category",
                 values_to = "Value") %>%
    mutate(Category = case_when(
      Category == "CClaw"  ~ "Civil & Commercial",
      Category == "CJlaw"  ~ "Criminal Justice",
      Category == "LLlaw"  ~ "Labour",
      Category == "PHlaw"  ~ "Public Health"
    ))
  
  ggplot(data2plot,
         aes(x       = reorder(Category, Value),
             y       = Value,
             label   = format(Value, big.mark = ","))) +
     geom_bar(fill   = "#9B8181",
              width  = 0.75,
              stat   = "identity") +
    geom_text(aes(y  = Value/2),
              family = "Fira Sans", 
              color  = "white") +
    coord_flip() +
    WJP_theme() +
    theme(panel.grid.major.x = element_line(size     = 0.5, 
                                            colour   = "grey93", 
                                            linetype = "solid"))
  
}


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Overview Map (NUTS PANEL)                                                                 ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

NUTSmap.fn <- function(selection) {
  
  # Defining data for map
  codes      <- NUTS.sf %>% filter(CNTR_NAME == selection) %>% pull(NUTS_ID)
  rec        <- NUTS.sf %>% filter(CNTR_NAME == selection) %>% pull(NAME_LATN)
  names(rec) <-  codes
  data4map <- MAPdata.sf %>%
    filter(NUTS_ID %in% codes) %>%
    group_by(location) %>%
    summarise(
      NUTS_ID = first(NUTS_ID),
      x = first(x),
      y = first(y),
      n = n()
    ) %>%
    st_as_sf(coords  = c("x", "y"),
             remove  = F,
             na.fail = F) 
  
  # Setting coordinates system for data
  st_crs(data4map) <- 4326
    
  # Creating the map
  ggplot() +
    geom_sf(data = NUTS.sf %>% 
              filter(CNTR_NAME == selection) %>%
              mutate(label = recode(NUTS_ID, !!!rec)),
            aes(fill = label),
            color    = "white") +
    geom_sf(data     = data4map,
            aes(text = paste("Location:", location),
                size = n),
            shape    = 1,
            color    = "#324A5F") +
    scale_fill_manual(name   = "Region",
                      values = nutsPalette) +
    theme_bw() +
    theme(panel.grid.major = element_blank(),
          legend.position  = "bottom",
          legend.box       = "vertical",
          legend.direction = "vertical",
          legend.text      = element_text(family = "Fira Sans", 
                                          face   = "plain", 
                                          size   = 8, 
                                          color  = "Black"),
          legend.title     = element_text(family = "Fira Sans", 
                                          face   = "bold", 
                                          size   = 9, 
                                          color  = "Black"), 
          axis.text        = element_text(family = "Fira Sans", 
                                          face   = "plain", 
                                          size   = 8, 
                                          color  = "Black")) +
    guides(size  = guide_legend(nrow  = 1, 
                                byrow = TRUE,
                                title = "Number of Lawyers"),
           fill  = guide_legend(nrow  = 2, 
                                byrow = TRUE))
}


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Summary NUTS Table (NUTS PANEL)                                                           ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

NUTSdt.fn <- function(selection) {
  NUTSdata.df %>%
    filter(country == selection) %>%
    select(
      `NUTS ID`                  = NUTS_ID,
      Region                     = NUTS_name,
      `No. of extracted Lawyers` = nlawyers,
      `Civil and Commercial`     = CClaw,
      `Criminal Justice`         = CJlaw,
      `Labour Law`               = LLlaw,
      `Public Health`            = PHlaw
    )
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Distribution Pie (NUTS PANEL)                                                             ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

NUTSdistribution.fn <- function(selection) {
  
  # Preparing data for pie charts
  data4pie <- NUTSdata.df %>%
    filter(country == selection) %>%
    select(
      Region               = NUTS_name,
      `Extracted Lawyers`  = nlawyers
    )
  
  if (nrow(data4pie) <= 5) {
    palette <- distpie_5
  } else if (nrow(data4pie) <= 8) {
    palette <- distpie_8
  } else {
    palette <- distpie_18
  }
  
  # Making the plotly
  plot_ly(data         = data4pie,
          labels       = ~Region, 
          values       = ~`Extracted Lawyers`, 
          type         = "pie",
          textposition = "inside",
          textinfo     = "label+percent",
          hoverinfo    = "text",
          text         = ~paste("Total Number of Lawyers:<br>",
                                format(`Extracted Lawyers`, 
                                       big.mark = ",")),
          textfont     = list(family = "Fira Sans"),
          marker       = list(colors = palette,
                              line   = list(color = "#FFFFFF", 
                                            width = 1)),
          showlegend   = T,
          domain       = list(row = 0, 
                              column = 0)) %>%
    layout(grid   = list(rows    = 1, 
                         columns = 2),
           xaxis  = list(showgrid       = F, 
                         zeroline       = F, 
                         showticklabels = F),
           yaxis  = list(showgrid       = F, 
                         zeroline       = F, 
                         showticklabels = F),
           legend = list(x = 0, 
                         y = 0,
                         orientation    = "h",
                         title          =list(text = "<b> Region </b>"))
    ) 
}


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                Gauge E-Mail (NUTS PANEL)                                                                 ----
##  
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

gaugeChart.fn <- function(selectionC, selectionN, value) {
  
  # Defining values for Gauge Charts depending on the value to display
  if (value == "email") {
    val <- NUTSdata.df %>%
      filter(country == selectionC & NUTS_name == selectionN) %>%
      mutate(perc = round((firm_email_bin/nlawyers)*100, 1)) %>%
      pull(perc)
    
    color <- "#3E503C"
    title <- "Percentage of Extracted Lawyers<br>with email address"
  }
  
  if (value == "phone") {
    val <- NUTSdata.df %>%
      filter(country == selectionC & NUTS_name == selectionN) %>%
      mutate(perc = round((phone_firm_bin/nlawyers)*100, 1)) %>%
      pull(perc)
    
    color <- "#8D3C01"
    title <- "Percentage of Extracted Lawyers<br>with phone number"
  }
  
  # Creating the plotly
  plot_ly(
    domain  = list(x = c(0, 1), 
                   y = c(0, 1)),
    value   = val,
    title   = list(text = title),
    type    = "indicator",
    mode    = "gauge+number",
    gauge   = list(
      bar   = list(color = color),
      axis  = list(range = list(NULL, 100)),
      steps = list(
        list(range = c(0, 25), 
             color = "gray"),
        list(range = c(25, 75), 
             color = "lightgray"))
      )
    ) %>%
    layout(
      margin = list(t = 30,
                    b = 10,
                    l = 20,
                    r = 30),
      font = list(color  = "darkblue", 
                  family = "Fira Sans"))
    
}
