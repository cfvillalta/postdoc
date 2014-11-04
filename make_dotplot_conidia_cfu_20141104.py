#! /usr/bin/python

#make dotplot of cfus from conidia germination experiments.

import sys

germination_data = sys.argv[1]
#file_name_split = germination_data.split("/")
#file_name_split_2 = file_name_split[6].split(".")

fh = open(germination_data)

csv = fh.readlines()

data = {}
#header = []

#print csv

cfu_300 = []
cfu_3000 = []
labels = [' ',' ','300',' ','3000']
for line in csv:
    if line.startswith("pCV"):
        line = line.strip()
        lines = line.split(",")
#        data_name = lines[1]
#        data[data_name] = lines
        cfu_3000.append(float(lines[1]))
        cfu_300.append(float(lines[2]))

data[3000]=cfu_3000
data[300]=cfu_300    
#print cfu_30
#print cfu_300
#print data

##############
#organzing data for graphing
##############
import numpy as np
import random
num = 0
y_axis_points = []
x_axis_points= []

for x in sorted(data):
    print x
    median = np.median(data[x])
    print "median %s" %(median)
    print "percentage of total = %s" %(100*(median/x))
    num = num+1
#    print num
    bioreps = 3
    a=num-.15
    b=num+.15
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    x_axis_points.extend(x_axis)
    y_axis_points.extend(data[x])

print num
print bioreps
print x_axis_points
print y_axis_points
import wx
import matplotlib as mpl
mpl.use('WXAgg')
import pylab

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax=plt.gca()
ax.set_xticklabels(labels, rotation =90)
plt.axis(ymin=0,ymax=500,xmin=0,xmax=num+1)
plt.plot(x_axis_points, y_axis_points, 'ro')
fig.tight_layout()
plt.show()
