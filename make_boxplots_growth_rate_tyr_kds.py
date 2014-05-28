#! /usr/bin/python

import sys
#input a file that is comma delimited csv.

growth_data = sys.argv[1]

fh = open(growth_data)

csv = fh.readlines()

data = {}
header = []

for line in csv:
    if line.startswith("pCV"):
        line = line.strip()
        lines = line.split(",")
        data_name = lines[0]
        data[data_name] = lines
        
    else:
         line = line.strip()
         lines = line.split(",")
         header = lines
        
    #print lines
    
    #print data

    #print header

#going to make boxplot
#http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
import numpy as np
import matplotlib as mpl

mpl.use('agg')

import matplotlib.pyplot as plt

boxplot_data = []

#made a dictionary with the key as vector...tyr1...tyr2...
tyrs = {}
for tyr in data:
    tyrs[data[tyr][2]]= ""


print tyrs
    # boxplot_data.append(float(data[tyr][1]))
    

    #print boxplot_data

    #fig = plt.figure(1, figsize=(9, 6))
    #ax = fig.add_subplot(111)
## Custom x-axis labels
#ax.set_xticklabels(['TYR1'])
#bp = ax.boxplot(boxplot_data)

#fig.savefig('fig1.png', bbox_inches='tight')

