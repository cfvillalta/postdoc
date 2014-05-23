#! /usr/bin/python

import sys
#input a file that is comma delimited csv.

growth_data = sys.argv[1]

fh = open(growth_data)

csv = fh.readlines()

data = {}

for line in csv:
    line = line.strip()
    lines = line.split(",")
    data = lines[1]

    #print lines
    

