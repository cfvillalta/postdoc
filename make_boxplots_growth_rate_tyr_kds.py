#! /usr/bin/python

import sys

growth_data = sys.argv[1]

fh = open(growth_data)

data = fh.readlines()

for line in data:
    line = line.strip()
    lines = line.split(",")

    print lines

