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

print data
#going to make a dotplot                                                                                             
'''
import numpy as np
import matplotlib as mpl
import pylab

#mpl.use('agg')                                                                                                    

import matplotlib.pyplot as plt

dotplot_data = []

#made a dictionary with the key as vector...tyr1...tyr2...                                                         
tyrs = {}
microconidia = {}
macrocondia = {}

for tyr in data:
    tyr_light = "%s_light" %(data[tyr][2])
    tyr_dark = "%s_dark" %(data[tyr][2])
    tyrs[tyr_light]= ""
    tyrs[tyr_dark]= ""
    growth_by_tyr[tyr_light] = []
    growth_by_tyr[tyr_dark] = []

    #print tyrs                                                                                                    
    #print data                                                                                                    

#lengths grouped by tyrosinases                                                                                    
for tyr in tyrs:
    for sample in data:
        # print sample                                                                                             
        #print tyr                                                                                                 
        if tyr == "%s_light" %(data[sample][2]):
            #growth_by_tyr[tyr] = append [data[sample]]                                                            
            growth_by_tyr[tyr].append(float(data[sample][3]))
            #print sample                                                                                          
        elif tyr == "%s_dark" %(data[sample][2]):
            growth_by_tyr[tyr].append(float(data[sample][5]))

tyr_sorted = []
tyr_growth_sorted = []
tyr_bioreps = []
tyr_sorted.append("")

#print growth_by_tyr                                                                                               

import random
num = 0
for x in sorted(growth_by_tyr):
    num = num+1
    print num
    tyr_sorted.append(x)
    tyr_growth_sorted.extend(growth_by_tyr[x])
    bioreps = len(growth_by_tyr[x])
    a=num-.15
    b=num+.15
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    tyr_bioreps.extend(x_axis)
print tyr_bioreps
print tyr_sorted
print tyr_growth_sorted



fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
## Custom x-axis labels                                                                                            
ax.set_xticklabels(tyr_sorted)

ax.set_xticklabels(tyr_sorted, rotation =90)
ax.set_ylabel('radial growth in cm')
ax.set_xlabel('tyroinase knockdowns grown in light or dark')
ax = plt.gca()
#ax.set_autoscale_on(False)                                                                                        


fig.savefig('fig1.png', bbox_inches='tight')
plt.tight_layout()
boxplot_name = "%s.png" %(file_name_split_2[0])



plt.axis(ymin=0,ymax=10)
plt.plot(tyr_bioreps, tyr_growth_sorted, 'ro')
fig.savefig(boxplot_name)
plt.show()
#I want to count lengths of list in growth by tyr dict.        
'''
