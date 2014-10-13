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
condition_list = ['']
for tyr in sorted(tyrs):
#    print tyr
    for cond in tyrs[tyr]:
#        print cond
         condition_list.append('%s_%s_microcondiia' %(tyr,cond))
         condition_list.append('%s_%s_macrocondiia' %(tyr,cond))
  #      for sample in  tyrs[tyr][cond]:
   #         print tyr
    #        print cond
     #       print sample
                    
#print sorted(data_to_plot.keys())
import numpy as np
dotplot_data=[]
#print data_to_plot
for name in sorted(data_to_plot.keys()):
#    print name
    name_split = name.split("_")
#    print name_split
    tyr_match = re.compile(name_split[0])
    cond_match = re.compile(name_split[1])
    add_list = []
#    microconidia
    for tyr in tyrs:
        for cond in tyrs[tyr]:
 #           condition_list.append('%s_%s_microcondiia' %(tyr,cond))
            for sample in tyrs[tyr][cond]:
                match = tyr_match.search(tyr)
                match_2 = cond_match.search(cond)
                
                if match and match_2:
                    #microconidia
                    add_list.append(np.log10(float(sample[4])))
                    
    dotplot_data.append(add_list)
    add_list=[]                    

#macroconidia
    for tyr in tyrs:
        for cond in tyrs[tyr]:
#            condition_list.append('%s_%s_microcondiia' %(tyr,cond))
            for sample in tyrs[tyr][cond]:
                match = tyr_match.search(tyr)
                match_2 = cond_match.search(cond)

                if match and match_2:
                    #macroconidia                                                
                    add_list.append(np.log10(float(sample[5])))
                    
    
    dotplot_data.append(add_list)
#all of the growth rate data /y axis ordered vector_light micro vector_ligth_marco then vector dark micro.....
print dotplot_data
print condition_list



##############
#organzing data for graphing
##############

import random
num = 0
y_axis_points = []
x_axis_points= []
for x in dotplot_data:
    num = num+1
    print num
    bioreps = len(x)
    a=num-.15
    b=num+.15
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    x_axis_points.extend(x_axis)
    y_axis_points.extend(x)


import matplotlib as mpl
mpl.use('WXAgg')
import pylab

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax=plt.gca()
ax.set_xticklabels(condition_list, rotation =90)
plt.axis(ymin=0,ymax=10,xmin=0,xmax=num+1)
plt.plot(x_axis_points, y_axis_points, 'ro')
fig.tight_layout()
plt.show()
