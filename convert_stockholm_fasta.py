#! /usr/bin/python


import sys

#input a stockholm formatted alignment.
stockholm_file = sys.argv[1]

file_name_split = stockholm_file.split(".")

print file_name_split
