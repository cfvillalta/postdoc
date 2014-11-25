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
#for each sample in data
for tyr in data:
	#add type of tyr underscore light and make new string
    tyr_light = "%s_light" %(data[tyr][2]
	#add type of tyr underscore dark and make new string  
    tyr_dark = "%s_dark" %(data[tyr][2])
	#make tyr light a key with empty string value
    tyrs[tyr_light]= ""
	#make tyr dark a key with empty string value 
    tyrs[tyr_dark]= ""
	#add tyr light as key to dixtionary with empty list. 
    growth_by_tyr[tyr_light] = []
	#add tyr light as key to dixtionary with empty list. 
    growth_by_tyr[tyr_dark] = []
#loop through tyr in tyrs
for tyr in tyrs:
	#loop through each sample in data. 
	for sample in data:
        #if genotype in tyr same as the genotype from data. 
		if tyr == "%s_light" %(data[sample][2]):
            #for tyr append growth data as floating point number
			growth_by_tyr[tyr].append(float(data[sample][3]))
        #else if tyr is equal to the growth rate of tyr in dark
        elif tyr == "%s_dark" %(data[sample][2]):
			#add growth data for tyr growing in dark. 
            growth_by_tyr[tyr].append(float(data[sample][5]))
#open blank list called tyr sorted. where i will put tyrs sorted alphabetically.           
tyr_sorted = []
#open blank list where i will lut growth rate numbers in by the alphabetical order of the correspondinf tyrs. 
tyr_growth_sorted = []
#open blank list where i will put tyr bioreps data.  
tyr_bioreps = []
#to tyr sorted list add a blank string. this is to make sure labels will look correct when graphed. 
tyr_sorted.append("")

import random
#set num integer to zero tonuse as a counter in loop
num = 0
#loop through sorted growth_by_tyr
for x in sorted(growth_by_tyr):
	#for each iteration add one to num
    num = num+1
	#print the num
    print num
	#add tyr to tyr_sorted list, now tyrs are ordered. 
    tyr_sorted.append(x)
#get data from dict with key and add to tyr_growth_sorted. 
   tyr_growth_sorted.extend(growth_by_tyr[x])
	#measure how many bioreos for each condition
    bioreps = len(growth_by_tyr[x])
	#set x axis range for data a is the max and b is the min distance
    a=num-.15
    b=num+.15
	#make a list of random numbers called x axis, amount of numbers in list dependent on number of bioreps. 
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)
	#add x-axis list to tyr_bioreps
    tyr_bioreps.extend(x_axis)
#create figure and set size. 
fig = plt.figure(1, figsize=(9, 6))
#add plot to figure
ax = fig.add_subplot(111)
#set Custom x-axis labels using tyr_sorted list. have labels be vertical at 90 degrees. 
ax.set_xticklabels(tyr_sorted, rotation =90)
#label y axis
ax.set_ylabel('radial growth in cm')
#label x-axis
ax.set_xlabel('tyroinase knockdowns grown in light or dark')
#type of graph
ax = plt.gca()
#make layout tight no extra space. 
plt.tight_layout()
#save to png with filepath and name similar to file input but different extension. in this case png. 
boxplot_name = "%s.png" %(file_name_split_2[0])
fig.savefig(boxplot_name)
#min and max of y axis. 
plt.axis(ymin=0,ymax=10)
#plot data to graph
plt.plot(tyr_bioreps, tyr_growth_sorted, 'ro')
#show graph. 
plt.show()

