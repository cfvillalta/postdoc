#!/usr/bin/python

#make dotplot of cfus from conidia germination experiments. I was just looking at one type of transformant and needed a quick graph.

import sys
#get filepath for germination data, file is in csv format.
germination_data = sys.argv[1]
#open file
fh = open(germination_data)
#readlines into list called csv
csv = fh.readlines()
#make an empty dictionary
data = {}
#list called cfu 300 for data from plates plated with 300 conidia
cfu_300 = []
#list called cfu 300 for data from plates plated with 3000 conidia
cfu_3000 = []
#labels for graph
labels = [' ',' ','300_BHI',' ','300_HMM',' ','3000_BHI']
#loop through csv list
for line in csv:
    #if line starts with pCV we know its a sample
    if line.startswith("pCV"):
        #strip line of whitespace
        line = line.strip()
        #split line into list by commas
        lines = line.split(",") 
        #see if the number below is a float
        try:
        #add cfus from plates plated with 3000 spores to cfu_3000 list.
            cfu_3000.append(float(lines[1]))
        #if number not a float then pass do not add to list
        except(ValueError):
            pass
        #try to see if number is a float
        try:
        #add cfus from plates plated with 300 spores to cfu_300 list.
            cfu_300.append(float(lines[2]))
        #if number is not a float then pass, do not add to list.
        except(ValueError):
            pass
#add each data set to dictionary of dictionaries called data. Subdictionary will have media information and a list with cfu counts.
data[300]={}
data[3000]={}
data[3000]['BHI']=cfu_3000
data[300]['HMM']=cfu_300[:3]
data[300]['BHI']=cfu_300[3:7]   
print data
##############
#organzing data for graphing
##############
import numpy as np
import random
#set number counter to zero, used to count number of conditions. In this case number of spore concentrations.
num = 0
#empty list to place y axis points.
y_axis_points = []
#empty list to place x axis points.
x_axis_points= []
#loop though sorted data dictionary
for x in sorted(data):
    #loop through dictionaries within dictionary.
    for media in data[x]:
    #get median of each set of conidia data using numpy
        median = np.median(data[x][media])
    #print the median 
        print "For media %s and %s spores plated the median was %s" %(media, x,median)
    #print percentage of total cfu from the original amount of spores plated.
        print "percentage of total = %s" %(100*(median/x))
    #add one to counter for each key/condition
        num = num+1
    #number of bioreps for each conidition
        bioreps = 3
    #min x-axis range
        a=num-.15
    #max x-axis range
        b=num+.15
    #assign random numbers between the min a and max b for the number of bioreps
        x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    #add the x-axis points to the list x_axis_points
        x_axis_points.extend(x_axis)
    #add y-axis points, e.g. cfu counts from the data dictionary to the list y axis points.
        y_axis_points.extend(data[x][media])

print x_axis_points
print y_axis_points

import wx
import matplotlib as mpl
#renderer to use for visualizing graphs in python
mpl.use('WXAgg')
import pylab
import matplotlib.pyplot as plt
#open a figure
fig = plt.figure()
#add a plot to the figure
ax = fig.add_subplot(111)
#define the type of plot being used.
ax=plt.gca()
#add x axis vertical labels.
ax.set_xticklabels(labels, rotation =90)
#define the min and max for the y and x axis
plt.axis(ymin=0,ymax=500,xmin=0,xmax=num+1)
#plot the data to the graph
plt.plot(x_axis_points, y_axis_points, 'ro')
#have a tight layout with not a lot of space
fig.tight_layout()
#show graph.
plt.show()
