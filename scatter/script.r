source('./r_files/flatten_HTML.r')

############### Library Declarations ###############
libraryRequireInstall("ggplot2");
libraryRequireInstall("plotly")
library("plotly")
library("ggplot2")
library("dplyr")
library("htmlwidgets")
####################################################

################### Actual code ####################
top_twenty <- Values %>% filter(rank(desc(Values$W3TZ))<=25)
doe_data <- data.frame(Values[Values$USDOELab == "yes",])
combo <- merge(top_twenty, doe_data, all=TRUE)
g = plot_ly() %>%
     add_trace(data = top_twenty, x = ~ScholarlyOutput, y = ~FWCI, type = 'scatter', mode=
     'markers', hoverinfo = 'text', text = ~paste('Institution: ', Institution, '\nScholary Output: ', ScholarlyOutput, '\nFWCI: ', FWCI, '\nCountry: ', Country), name = 'Top 20', marker=list(size = 20, opacity = 0.5, color = ~as.character(Colors))) %>% 
     add_trace(data = doe_data, x = ~ScholarlyOutput, y = ~FWCI, type = 'scatter', mode= 'markers', hoverinfo= 'text', text = ~paste('Institution: ', Institution, '\nScholary Output: ', ScholarlyOutput, '\nFWCI: ', FWCI), name = 'DOE Labs', marker = list(size=10, opacity = 0.5, color = 'green')) %>%
     add_annotations(data = combo, x = ~ScholarlyOutput, y = ~FWCI, xref = 'x', yref = 'y', xanchor = 'right', yanchor = 'bottom', text = ~Abbreviation, showarrow = FALSE, clicktoshow = 'onoff')  %>%
	 layout(xaxis = list(title = 'Scholarly Output'),
	 yaxis = list(title = 'FWCI'))

####################################################

############# Create and save widget ###############
p = ggplotly(g);
internalSaveWidget(p, 'out.html');
####################################################
