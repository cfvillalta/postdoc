#! /usr/bin/python

import sys
#input a file that is comma delimited csv.

growth_data = sys.argv[1]
file_name_split = growth_data.split("/")
#print file_name_split[6]
file_name_split_2 = file_name_split[6].split(".")

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

print growth_by_tyr

for x in sorted(growth_by_tyr):
    tyr_sorted.append(x)
    tyr_growth_sorted.append(growth_by_tyr[x])

    #print tyr_sorted
    #print tyr_growth_sorted
fig = plt.figure(1, figsize=(9, 6))
#fig = plt.figure(1)
ax = fig.add_subplot(111)
## Custom x-axis labels
ax.set_xticklabels(tyr_sorted)
ax.boxplot(tyr_growth_sorted)
plt.axis(ymin=0,ymax=10)
ax.set_xticklabels(tyr_sorted, rotation =90)
ax = plt.gca()
#ax.set_autoscale_on(False)

plt.show()
#fig.savefig('fig1.png', bbox_inches='tight')
plt.tight_layout()
boxplot_name = "%s.png" %(file_name_split_2[0])
fig.savefig(boxplot_name)
