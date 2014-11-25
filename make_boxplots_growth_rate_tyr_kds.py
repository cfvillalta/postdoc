#! /usr/bin/python

import sys
#use  a file that is comma delimited csv.
#get filepath to csv file
growth_data = sys.argv[1]
#split filename by backslash.
file_name_split = growth_data.split("/")
#split filepath by . to separate path from extension.
file_name_split_2 = file_name_split[6].split(".")
#open growth_data
fh = open(growth_data)
#read lines into csv list.
csv = fh.readlines()
#create blank dictionary
data = {}
#create blank list.
header = []
#loop through csv list
for line in csv:
    #if line starts with pCV
    if line.startswith("pCV"):
        #strip whitespace at ends
        line = line.strip()
        #split line by comma and put data into lines list
        lines = line.split(",")
        #copy the second variable in the list to data_name
        data_name = lines[1]
        #make data name the key e.g. pCV168 and add the list lines as the value of each entry into the dictionary called data.
        data[data_name] = lines
    #line does not start with pCV
    else:
        #strip line of whitespace
        line = line.strip()
        #split at comma into list called lines
        lines = line.split(",")
        #copy contents of lines into list called header.
        header = lines        
#going to make boxplot
#http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import pylab
#create empty list to place boxplot data.
boxplot_data = []
#create an empty dictionary to place data in by tyrosinase.
tyrs = {}
#another empty dictionary to place data in by tyrosinase
growth_by_tyr = {}
for tyr in data:
    tyr_light = "%s_light" %(data[tyr][2])
    tyr_dark = "%s_dark" %(data[tyr][2])
    tyrs[tyr_light]= ""
    tyrs[tyr_dark]= ""
    growth_by_tyr[tyr_light] = []
    growth_by_tyr[tyr_dark] = []
#STOPPED HERE
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
    #print tyr_bioreps
    #print tyr_sorted
    #print tyr_growth_sorted



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
fig.savefig(boxplot_name)


plt.axis(ymin=0,ymax=10)
plt.plot(tyr_bioreps, tyr_growth_sorted, 'ro')
plt.show()


#I want to count lengths of list in growth by tyr dict.

