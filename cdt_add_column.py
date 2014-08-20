#!/usr/bin/env python

#will input cdt file
#extract GID
#search for GID with BLASTDBCMD

import sys


cdt_input = sys.argv[1]

cdt_input_split = cdt_input.split(".")

cdt_in =open(cdt_input, 'r')

############
#Pushed everything into a dictory with a list of each type of column from the cdt. Should be no dups in the GID
############
cdt_original = cdt_in.readlines()
#print cdt_original
header = ''
eweight = ''
cdt_dict = {}
for line in cdt_original:
    #print line
    line = line.strip()
    if line.startswith('GID'):
        header = line
        print header
    
    elif line.startswith('EWEIGHT'):
        eweight = line
        print eweight
    else:
        line_split = line.split('\t')
        get_GID = line_split[0].split('/')
        GID = get_GID[0]
        cdt_dict[GID] = line_split

print cdt_dict

###################
#Use Blastdbcmd to get all the tax_ids from nr and add that to a new column in array it will be between GWEIGHT and dummy. Will call TAXID

