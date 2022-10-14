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
## This version:      October 13th, 2022
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
##                Qualified Experts                                                                         ----
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



