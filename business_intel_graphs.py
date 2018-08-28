#This program assumes you're working with a spreadsheet that has 4 specific columns (more are fine, but these must be present)
#| abbname | Colors | ScholarlyOut | FWCIA |
#The order does not matter, but the spelling/capitalization does (so change the code below if your sheet looks different)
#NOTE: the adjust_text function will optimize labels; but, after rendering, you can drag labels manually for fine-tuning before saving graphic
#
#!Python 3.5
#run with Anaconda

import os
import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text
import seaborn as sns

withChina = True
noChina = False
allGovernment = False
noChinaGovernment = False
specialRequest = False
allLabs = False
indLabs = True

#Change filename and path according to what spreadsheet is titled + filepath
filename = 'isos.xlsx'
path = 'C:\\Users\\vkk\\Desktop\\JIBS\\'

def makeGraph(data, labData):

#add light gray background to plot, remove black rectangle frame
	sns.set_style('darkgrid')
	sns.set_context('talk')

#loop through columns in spreadsheet to get x and y axis, colors
	plt.scatter(x = data['ScholarlyOut'], 
				y = data['FWCIA'],
				s = 900,
				c = data['Colors'],
				alpha = 0.6, 
				edgecolors= 'b',
				linewidth=2)

#Add Laboratory data to graph
	plt.scatter(x = labData['ScholarlyOutLab'],
				y = labData['FWCILab'],
				s = 900,
				c = labData['Colors'],
				alpha = 0.6,
				edgecolors = 'none',
				linewidth = 2)


#add title, axis labels, and grid to graph
	#plt.title('Benchmarking Advanced Reactors', fontsize = 22)
	plt.xlabel('Scholarly Output', fontsize = 16)
	plt.ylabel('FWCI', fontsize = 16)
	plt.grid(True)

#save labels to list to adjust position later
	texts= []

#add labels to graph plots and append the texts list for adjustment
	for name in range(len(data['abbname'])):
		texts.append(plt.text(x = data['ScholarlyOut'][name], 
							  y = data['FWCIA'][name], 
							  s = data['abbname'][name], 
							  fontsize = 16, 
							  color = data['Colors'][name] 
	))

#add laboratory labels
	for name in range(len(labData['abbnameLab'])):
		texts.append(plt.text(x = labData['ScholarlyOutLab'][name],
							  y = labData['FWCILab'][name],
							  s = labData['abbnameLab'][name],
							  fontsize = 16,
							  color = labData['Colors'][name]
			))

#adjust labels for plot points
	adjust_text(texts)

	
if withChina:
	data = pd.read_excel(path + filename, sheetname=2, skiprows=3, parse_cols='G:K', index_col=False).dropna()

if noChina: 
	data = pd.read_excel(path + filename, sheetname=3, skiprows=3, parse_cols='G:K', index_col=False).dropna()
	
if allGovernment:
	data = pd.read_excel(path + filename, sheetname=2, skiprows=2, parse_cols='G:K', index_col=False).dropna()
	
if noChinaGovernment:
	data = pd.read_excel(path + filename, sheetname=3, skiprows=3, parse_cols='G:K', index_col=False).dropna()
	
if specialRequest:
	data = pd.read_excel(path + filename, sheetname=6, skiprows=3, parse_cols='A:E', index_col=False).dropna()
	
if indLabs:
	labData = pd.read_excel(path + filename, sheetname=4, skiprows=3, parse_cols='B:F', index_col=False).dropna()

if allLabs:
	labData = pd.read_excel(path + filename, sheetname=5, skiprows=3, parse_cols='A:D', index_col=False).dropna()

makeGraph(data, labData)

#display the graph
plt.show()
