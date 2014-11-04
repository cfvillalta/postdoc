#! /usr/bin/python

#make dotplot of cfus from conidia germination experiments.

import sys

germination_data = sys.argv[1]
file_name_split = growth_data.split("/")
file_name_split_2 = file_name_split[6].split(".")

fh = open(growth_data)

csv = fh.readlines()

data = {}
header = []

print csv
