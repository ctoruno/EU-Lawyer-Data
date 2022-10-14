## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Script:            EU Lawyer data - Functions
##
## Author:            Carlos A. Toruño Paniagua   (ctoruno@worldjusticeproject.org)
##
## Dependencies:      World Justice Project
##
## Creation date:     May 28th, 2022
##
## This version:      June 9th, 2022
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## Outline:                                                                                                 ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                0.  Presetting                                                                            ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Defining color palette according to WJP Manual of Style
WJPcolorPalette <- c("#f4cc21", "#eb9727", "#f05b42", "#d12241", "#91288c", "#2d3589", "#2779bd",
                     "#2ba7a4", "#90d1eb")
WJPheatPalette <- c("#e41e27", "#ed592d", "#f2a340", "#f4c715", "#ccc454", "#9cba8f", "#548c7d", "#0d4f52")

# Defining a WJP theme function
WJP_theme <- function(){
  theme(legend.title = element_blank(),
        legend.text = element_markdown(size = 7, 
                                       family = "Lato Full", 
                                       face = "bold", 
                                       margin = margin(0, 0, 0, -4)),
        legend.spacing.x = unit(0.1, "mm"),
        panel.background = element_rect(fill = "white", 
                                        size = 2),
        panel.grid.major.x = element_line(size = 0.5, 
                                          colour = "grey93", 
                                          linetype = "solid"),
        panel.grid.minor = element_blank(),
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        axis.text.y  = element_text(family = "Lato Full", 
                                    face = "plain", 
                                    size = 3*.pt, 
                                    color = "Black"),
        axis.text.x = element_text(family = "Lato Full", 
                                   face = "bold", 
                                   size = 3*.pt, 
                                   color = "Black"),
        axis.ticks = element_blank(),
        axis.line.y.left = element_line(size = 1.5, 
                                        colour = "black", 
                                        linetype = "solid"),
        plot.subtitle = element_text(family = "Lato Full", 
                                     face = "italic", 
                                     size = 11, 
                                     color = "Black",
                                     margin = margin(0, 0, 15,0)),
        plot.title = element_text(family="Lato Black", 
                                  size = 14, 
                                  color = "Black", 
                                  margin = margin(15, 0, 5, 0)),
        plot.title.position = "plot",
        plot.caption = element_text(family="Lato Full", 
                                    face = "italic",
                                    size = 8, 
                                    color = "Black")) 
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                1.  Webscrapping general results                                                          ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

results_panel.fn <- function(data, reg){
  
  # Preparing data for plot
  data2plot <- data %>%
    st_drop_geometry() %>%
    summarise(`Mapped individuals`                = n(), 
              `Individuals with<br>email data`       = sum(firm_email_bin, na.rm = T)) %>%
    mutate(`No. of registered<br>lawyers (EUROSTAT)` = reg) %>%
    pivot_longer(everything(),
                 values_to = "No. of Lawyers",
                 names_to  = "Category")
  
  # Make the plot
  ggplot(data  = data2plot, 
         aes(x = Category, 
             y = `No. of Lawyers`)) +
    geom_col(fill ="#2779bd") +
    geom_text(aes(y     = `No. of Lawyers`/2,
                  label = format(`No. of Lawyers`, 
                                 big.mark = ",")),
              color     = "white",
              size      = 3,
              fontface  = "bold") +
    scale_y_continuous(expand = c(0,0),
                       limits = c(0, max(data2plot$`No. of Lawyers` + 500))) +
    WJP_theme() +
    theme(axis.line.x.bottom = element_line(size = 2.5, 
                                            colour = "black", 
                                            linetype = "solid"))
}


## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                2.  Specializations                                                                       ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

specialization_panel.fn <- function(data){
  
  "%!in%" <- compose("!", "%in%")
  
  # Preparing data for plot
  data2plot <- data %>%
    st_drop_geometry() %>%
    mutate(sum   = rowSums(across(c(CClaw, CJlaw, LLlaw, PHlaw))),
           QRQ = if_else(sum == 0, "Does not qualify for QRQ", "Qualifies for QRQ")) %>%
    count(QRQ)
  
  # Make the plot
  PanelA <- ggplot(data2plot, aes(y = n,
                                  x = QRQ)) +
    geom_bar(fill = "#0d4f52",
             stat = "identity") +
    geom_text(aes(y     = n/2, 
                  label = format(n, big.mark = ",")), 
              color     = "white",
              size      = 3,
              fontface  = "bold") +
    scale_y_continuous(expand = c(0,0)) +
    coord_flip() +
    theme(legend.position = "none",
          panel.background = element_rect(fill = "white", 
                                          size = 2),
          panel.grid.major.x = element_line(size = 0.5, 
                                            colour = "grey93", 
                                            linetype = "solid"),
          panel.grid.minor = element_blank(),
          axis.title.y = element_blank(),
          axis.title.x = element_blank(),
          axis.line.y.left = element_line(size = 1.5, 
                                          colour = "black", 
                                          linetype = "solid"))
  
  data2plot <- data %>%
    st_drop_geometry() %>%
    select(CClaw, CJlaw, LLlaw, PHlaw) %>%
    summarise(CClaw = sum(CClaw, na.rm = T),
              CJlaw = sum(CJlaw, na.rm = T),
              LLlaw = sum(LLlaw, na.rm = T),
              PHlaw = sum(PHlaw, na.rm = T)) %>%
    pivot_longer(everything(),
                 names_to = "category",
                 values_to = "totalValue") %>%
    mutate(category = case_when(
      category == "CClaw" ~ "Civil and Commercial",
      category == "CJlaw" ~ "Criminal Justice",
      category == "LLlaw" ~ "Labor Law",
      category == "PHlaw" ~ "Public Health",
    ))
  
  PanelB <-ggplot(data = data2plot, 
                  aes(x = category, 
                      y = totalValue)) +
    geom_col(fill ="#2779bd") +
    geom_text(aes(y     = totalValue/2,
                  label = format(totalValue, 
                                 big.mark = ",")),
              color     = "white",
              size      = 3,
              fontface  = "bold") +
    scale_y_continuous(expand = c(0,0),
                       limits = c(0, max(data2plot$totalValue + 2500))) +
    coord_flip() +
    WJP_theme()
  
  return(list(PanelA, PanelB))
  
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                3.  Top specializations                                                                   ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

topspecs_panel.fn <- function(data){

  "%!in%" <- compose("!", "%in%")

  # Preparing data to plot
  data2plot <- data %>%
    st_drop_geometry() %>%
    {if ("BE1" %in% data$NUTS_ID) filter(., phone_firm_bin == 1) 
      else filter(., phone_firm_bin == 1 | firm_email_bin == 1)} %>%
    select(starts_with("spec_english_")) %>%
    pivot_longer(everything(),
                 names_to = "column",
                 values_to = "spec_english") %>%
    select(spec_english) %>%
    filter(!is.na(spec_english)) %>%
    filter(spec_english %!in% "-") %>%
    filter(spec_english %!in% c("", "N / A")) %>%
    mutate(spec_english = tolower(spec_english),
           spec_english = trimws(spec_english)) %>%
    group_by(spec_english) %>%
    count() %>%
    arrange(desc(n)) %>%
    mutate(percentage = paste0(round(n/nrow(data)*100, 0), "%"))
  
  # Plotting data
  if("BE1" %in% data$NUTS_ID){
    dist4axis1 <- 125
    dist4axis2 <- 50
    int4axis   <- 200
  } else {
    dist4axis1 <- 325
    dist4axis2 <- 100
    int4axis   <- 500
  }

  ggplot(data = data2plot[1:25,],
         aes(x = reorder(spec_english, n),
             y = n,
             label = percentage)) +
    geom_point(size = 2,
               color = "#eb9727") +
    labs(y     = "Number of mentions") +
    scale_y_continuous(breaks = seq(0, max(data2plot$n) + dist4axis2,
                                    by = int4axis)) +
    coord_flip(clip = "off",
               ylim = c(0, max(data2plot$n) + dist4axis2)) +
    WJP_theme() +
    theme(legend.position = "top",
          legend.key = element_rect(fill = "white"),
          panel.grid.major.y = element_line(size = 0.5,
                                            colour = "grey65",
                                            linetype = "solid"),
          panel.grid.major.x = element_blank(),
          axis.title.x = element_text(family = "Lato Full",
                                      face   = "bold",
                                      size   = 3*.pt,
                                      color  = "Black",
                                      margin = margin(5, 0, 0, 0)),
          axis.text.x = element_text(family = "Lato Full",
                                     face = "plain",
                                     size = 2*.pt,
                                     color = "Black"),
          plot.margin = unit(c(0.5, 2, 0.5, 0.5), "lines"))
  
}

## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##                4.  Top firms                                                                             ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

top_firms_panel.fn <- function(data){
  
  nodata <- nrow(data) == sum(is.na(data$firm_name))
  
  firmData <- data %>%
    st_drop_geometry() %>%
    group_by(firm_name, location) %>%
    filter(!is.na(location)) %>%
    count(name = "nlawyers") %>%
    ungroup() %>%
    slice_max(nlawyers, n = 10, with_ties = T) %>%
    rename(`Firm Name`      = firm_name,
           Location         = location,
           `No. of lawyers` = nlawyers)
  
  if (nodata == T) {
    return(firmData[NULL,])
  } else {
    return(firmData)
  }
}
