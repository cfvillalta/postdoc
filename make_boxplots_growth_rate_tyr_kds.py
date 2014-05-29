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
        data_name = lines[1]
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
growth_by_tyr = {}
for tyr in data:
    tyrs[data[tyr][2]]= ""
    growth_by_tyr[data[tyr][2]] = []


    #print tyrs
    #print data

#lengths grouped by tyrosinases
for tyr in tyrs:
    for sample in data:
        # print sample
        #print tyr
        if tyr == data[sample][2]:
            #growth_by_tyr[tyr] = append [data[sample]] 
            #print tyr
            growth_by_tyr[tyr].append(data[sample][3])
            #print sample
    # boxplot_data.append(float(data[tyr][1]))
            
    # print growth_by_tyr
            
    #print boxplot_data



    x = growth_by_tyr.keys()
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
## Custom x-axis labels
    ax.set_xticklabels(growth_by_tyr.keys())
#bp = ax.boxplot(boxplot_data)

#fig.savefig('fig1.png', bbox_inches='tight')
