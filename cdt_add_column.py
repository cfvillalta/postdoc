#!/usr/bin/env python

#will input cdt file
#extract GID
#search for GID with BLASTDBCMD

import sys
from subprocess import Popen, PIPE


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
num=0
for line in cdt_original:
    #print line
    line = line.strip()
    if line.startswith('GID'):
        header = line
        header_split = header.split("\t")
        header_split.insert(5, "TAXID")
        header = "\t".join(header_split)
        #print header
    elif line.startswith('EWEIGHT'):
        eweight = line
        eweight_split = eweight.split("\t")
        eweight_split.insert(5,"\t")
        eweight = "\t".join(eweight_split)
        #print eweight
    else:
        num = num+1
        line_split = line.split('\t')
        #        get_GID = line_split[0].split('/')
        GID = line_split[0]
        # print GID
        cdt_dict[num] = line_split

        #print cdt_dict

###################
#Use Blastdbcmd to get all the tax_ids from nr and add that to a new column in array
#it will be between GWEIGHT and dummy. Will call TAXID.
###################

for GID in cdt_dict:
    GID_split = cdt_dict[GID][0].split('/')
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    stdout = p.stdout.read()
    p.communicate()
    if stdout:
        ID = stdout.strip()
        ID = ID.replace(' ', '_')  
        ID = ID.replace('[', '')
        ID = ID.replace(']', '')
        ID = ID.replace(',', '_')
        ID = ID.replace('/', '_')
        ID = ID.replace('__', '_')
        ID = ID.replace(':', '_')
        ID = ID.replace('.', '_')
        ID = ID.replace('(', '_')
        ID = ID.replace(')', '_')
        ID = ID.replace(';', '_')
        ID = ID.replace('+', '_')
        ID = ID.replace('=', '_')
        ID = ID.replace('__', '_')
        ID = ID.replace('__', '_')
        ID = ID.replace('__', '_')
        #print ID
       
        cdt_dict[GID].insert(5, ID)
    else:  
        cdt_dict[GID].insert(5, GID_split[0])
        

#print cdt_dict
####################
#join everything together
###################

#print
cdt_mod = open("%s_mod.cdt" %(cdt_input_split[0]),'w')

cdt_mod.write('%s\t\n' %(header))
cdt_mod.write('%s\t\n' %(eweight))
for row in sorted(cdt_dict.keys()):
    #    print row
    #print cdt_dict[row]
    cdt_mod.write('%s\t\n' %("\t".join(cdt_dict[row])))





cdt_mod.close()

    
