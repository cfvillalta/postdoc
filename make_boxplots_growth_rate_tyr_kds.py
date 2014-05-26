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
        data_name = lines[0]
        data[data_name] = lines
        
    else:
         line = line.strip()
         lines = line.split(",")
         header = lines
        
    #print lines
    
    #print data

    #print header

#going to make boxplot
from pylab import *

boxplot_data = []

for light in data:
    boxplot_data.append(float(data[light][2]))
    

print boxplot_data
figure()
boxplot(boxplot_data)
