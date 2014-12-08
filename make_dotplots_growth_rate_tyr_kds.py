#!/usr/bin/env/python

import sys
#get filepath for comma delimited csv with tyr data.
growth_data = sys.argv[1]
#split filepath by backslash
file_name_split = growth_data.split("/")
#split filepath by . to separate filepath from extension.
print file_name_split
file_name_split_2 = file_name_split[5].split(".")
#open csv file
fh = open(growth_data)
#read lines into list called csv.
csv = fh.readlines()
#open a empty dicitonary called data
data = {}
#open blank list called header.
header = []
#loop through list csv
for line in csv:
    #if line starts with pCV run code below
    if line.startswith("pCV"):
        #strip whitespace from line
        line = line.strip()
        #split the line by comma and put into lines list.
        lines = line.split(",")
        #name of sample will be copied into string data_name.
        data_name = lines[1]
        #data_name will be key in data dict and the lines list will be value.
        data[data_name] = lines
    #else not pCV run code below.
    else:
        #strip white space
        line = line.strip()
        #split by comma
        lines = line.split(",")
        #copy list to empty header list.
        header = lines
        
#going to make boxplot
#http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
import numpy as np
import matplotlib as mpl
import pylab
import matplotlib.pyplot as plt
#make an empty list where I will put boxplot_data
boxplot_data = []
#make a blank dictionary where I will place each type of tyr present as key and will add a blank string
tyrs = {}
#make a blank dictionary where I will place each type of tyr present as a key and will add a blank list
growth_by_tyr = {}
#loop through data dict
for tyr in data:
    #create a genotype_light for each genotype
    tyr_light = "%s_light" %(data[tyr][2])
    #create a genotype_dark for each genotype
    tyr_dark = "%s_dark" %(data[tyr][2])
    #use tyr_light and tyr_dark as key for dictionary tyrs
    tyrs[tyr_light]= ""
    tyrs[tyr_dark]= ""
    #use tyr_light and tyr_dark as key for dictionary growth_by_tyr
    growth_by_tyr[tyr_light] = []
    growth_by_tyr[tyr_dark] = []
#lengths grouped by tyrosinases
#loop through each genotype/coniditon in tyrs.
for tyr in tyrs:
    #loop through each sample in the data dict.
    for sample in data:
        #if the tyr is equal to the tyr in the data and light
        if tyr == "%s_light" %(data[sample][2]):
            #get data for the genotype and condition combination and convert to floating numbers. Add that data to the list for the the specific genotype/condition key in growth_by_tyr dictionary.
            growth_by_tyr[tyr].append(float(data[sample][3]))
        #if the tyr is equal to the tyr in  the data and the dark condition.
        elif tyr == "%s_dark" %(data[sample][2]):
            #get data for the genotype and condition combintation and convert to floating numbers. Add that data to the list for the specific genotype/condition key in the growth_by_tyr dictionary.
            growth_by_tyr[tyr].append(float(data[sample][5]))
 #make a blank list called tyr_sorted where genotype_condition will be sorted alphabetically           
tyr_sorted = []
#make a blank list called tyr_growth_sorted where growth data is sorted alphabetically by condition.
tyr_growth_sorted = []
#make a list of how many bioreps for each condition.
tyr_bioreps = []
#add a blank string to tyr_sorted. For formatting of x-axis tick labels purpose.
tyr_sorted.append("")

import random
#make a number counter set to zero
num = 0
#sort the dict growth_by_tyr by key and loop through each key.
for x in sorted(growth_by_tyr):
    #add one to counter
    num = num+1
    #add the key (genotype_condition) to a list called tyr_sorted.
    tyr_sorted.append(x)
    #extend list tyr_growth_sorted by measurment data for each key
    tyr_growth_sorted.extend(growth_by_tyr[x])
    #determine how many bioreps/measurements for each condition
    bioreps = len(growth_by_tyr[x])
    #min for x-axis coordinates
    a=num-.15
    #max for x-axis coordinates
    b=num+.15
    #add random number of x axis coordinated between the min a and max b corresponding to the number of bioreps.
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    #add list of x_axis cordinated to the tyr_bioreps list.
    tyr_bioreps.extend(x_axis)
#make new figure
fig = plt.figure(1, figsize=(9, 6))
#add plot to figure
ax = fig.add_subplot(111)
#add Custom x-axis tick labels
ax.set_xticklabels(tyr_sorted, rotation =90)
#add y axis label
ax.set_ylabel('radial growth in cm')
#add x axis label
ax.set_xlabel('tyroinase knockdowns grown in light or dark')
#set type of graph
ax = plt.gca()
#make a tight layout no large extra space.
plt.tight_layout()
#filepath for .png file where plot data will be drawn
boxplot_name = "%s.png" %(file_name_split_2[0])
#set the number of xticks
ax.set_xticks(np.arange(0,(num+1),1))
#y axis min and max
plt.axis(ymin=0,ymax=10,xmin=0, xmax=num+1)
#plot the graph with the data in brackets
plt.plot(tyr_bioreps, tyr_growth_sorted, 'ro')
#save plot to .png file
fig.savefig(boxplot_name)
#show plot in python
plt.show()


