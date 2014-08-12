#! /usr/bin/python/

import subprocess as sp
import os
import sys

program = 'tar'

folder_tars = sys.argv[1]
print folder_tars

files = os.listdir (folder_tars)


for file in files:
    print file
