#!/usr/bin/env python

#script will input csv file and then make dotplot of data. 
#calculte the median and plot it a different color or shape...

import sys
import re

conidia_data = sys.argv[1]
file_name_split = conidia_data.split(".")

fh = open(conidia_data)

csv = fh.readlines()

data = {}
header = []

for line in csv:
    sample = re.compile(r"(pCV\d+\-\d)")
    match = sample.search(line)
    if match:
        line = line.strip()
        lines = line.split(",")
        data_name = lines[0]
        data[data_name] = lines

    else:
         line = line.strip()
         lines = line.split(",")
         header = lines

#print data

#going to organize data by tyr.

tyrs = {}
for sample in data:

    if data[sample][2] in tyrs:

        if data[sample][3] in tyrs[data[sample][2]]:
           # print '%s if tyr present, and light or dark' %(data[sample])
            tyrs[data[sample][2]][data[sample][3]].append(data[sample])
        else:


            tyrs[data[sample][2]][data[sample][3]]=[data[sample]]
    else:
       # print '%s if tyr not present yet' %(data[sample])
        
        tyrs[data[sample][2]]={}
        tyrs[data[sample][2]][data[sample][3]]=[data[sample]]


#tyrs e.g. vector_light, vector_dark,tyr_light, tyr_dark
data_to_plot = {}
num_cond = 0
for tyr in tyrs:
    for cond in tyrs[tyr]:
        num_cond = num_cond+1
        data_to_plot["%s_%s" %(tyr, cond)]= []
#print tyrs
#for tyr in tyrs:
#    print tyr
 #   for cond in tyrs[tyr]:
 #       print cond
  #      for sample in  tyrs[tyr][cond]:
   #         print tyr
    #        print cond
     #       print sample
                    
#print sorted(data_to_plot.keys())

dotplot_data=[]
for name in sorted(data_to_plot.keys()):
 #   print data_to_plot[name]
    name_split = name.split("_")
#    print name_split
    tyr_match = re.compile(name_split[0])
    cond_match = re.compile(name_split[1])
    add_list = []
#    microconidia
    for tyr in tyrs:
        for cond in tyrs[tyr]:
            for sample in tyrs[tyr][cond]:
                match = tyr_match.search(tyr)
                match_2 = cond_match.search(cond)
                
                if match and match_2:
                    #microconidia
                    add_list.append(sample[4])
    dotplot_data.append(add_list)
    add_list=[]                    
#macroconidia
    for tyr in tyrs:
        for cond in tyrs[tyr]:
            for sample in tyrs[tyr][cond]:
                match = tyr_match.search(tyr)
                match_2 = cond_match.search(cond)

                if match and match_2:
                    #macroconidia                                                
                    add_list.append(sample[5])
    
    dotplot_data.append(add_list)
import random
print dotplot_data
num_conds = len(dotplot_data)
num_conds_list =  [random.uniform(a,b) for p in range(0, num_conds)]
import numpy as np
import matplotlib as mpl
import pylab

#mpl.use('agg')

import matplotlib.pyplot as plt
#plt.plot(
