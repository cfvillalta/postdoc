#!/usr/bin/env python
#this script takes in a CDT file used to visiaulize data in java treeview. In my case usually a phylogenetic tree. The script takes in the CDT and adds a new column with taxonomic data e.g. species name from NCBI nr database. The script uses blastdbcmd.
#will input cdt file
#extract GID
#search for GID with BLASTDBCMD

import sys
from subprocess import Popen, PIPE

#input cdt file
cdt_input = sys.argv[1]
#split the file name and extension at "."
cdt_input_split = cdt_input.split(".")
#open cdt file
cdt_in =open(cdt_input, 'r')

############
#Pushed everything into a dictory with a list of each type of column from the cdt. Should be no dups in the GID
############
#read lines into list from the cdt file.
cdt_original = cdt_in.readlines()
#make string called header
header = ''
#make string called eweight
eweight = ''
#make dictionary called cdt_dict
cdt_dict = {}
#make an num 0 to be used to count.
num=0
#loop through list of cdt_original
for line in cdt_original:
    #strip whitespace. 
    line = line.strip()
    #if line starts with GID
    if line.startswith('GID'):
        #add line to header
        header = line
        #split the header by \t
        header_split = header.split("\t")
        #insert the TAXID into list at the 5th position
        header_split.insert(5, "TAXID")
        #join header.split and overwrite old header.
        header = "\t".join(header_split)
    #if line begins with EWEIGHT
    elif line.startswith('EWEIGHT'):
        #copy line into eweight.
        eweight = line
        #split ewight by \t
        eweight_split = eweight.split("\t")
        #insert a blank space as a \t
        eweight_split.insert(5,"\t")
        join all eweight by \t
        eweight = "\t".join(eweight_split)
    #if line is non of the above
    else:
        #add 1 to counter.
        num = num+1
        #split line by \t.
        line_split = line.split('\t')
        #split data is input into cdt_dict with the number of the iteration as the key.
        cdt_dict[num] = line_split
###################
#Use Blastdbcmd to get all the tax_ids from nr and add that to a new column in array
#it will be between GWEIGHT and dummy. Will call TAXID.
###################
#loop through cdt_dict.
for GID in cdt_dict:
    #from list in cdt_dict grab the string with the GID inside and then split the GID from the sequence infor after the backslash.
    GID_split = cdt_dict[GID][0].split('/')
    #use Popen to run blastdbcmd as a subprocess. blastdbcmd will run and find the taxonomic information of specific GID.
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    #extract the output from blastcmd
    stdout = p.stdout.read()
    #wait until subprocess is done until the script continues forward.
    p.communicate()
    #if there is a stdout meaning that information for the GID was present in NR
    if stdout:
        #strip and replace all the charctaers with either whitespace or '_' 
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
        #insert ID into the fifth position of the list for the current GID within the dict
        cdt_dict[GID].insert(5, ID)
    #if no output from the subprocess found
    else:  
        #just insert the GID into the fifth positon of the list for the GID we are accessing from the dict.
        cdt_dict[GID].insert(5, GID_split[0])
####################
#join everything together
###################
#open new cdt file and use the same file name with the addition of _mod.cdt
cdt_mod = open("%s_mod.cdt" %(cdt_input_split[0]),'w')
#write modified header to modified cdt.
cdt_mod.write('%s\t\n' %(header))
#write modified eweight line to modified cdt.
cdt_mod.write('%s\t\n' %(eweight))
#loop through cdt_dict keys in numerical order 
for row in sorted(cdt_dict.keys()):
    #write each GID and its information onto new modified cdt file.
    cdt_mod.write('%s\t\n' %("\t".join(cdt_dict[row])))




#close new modified file. script done.
cdt_mod.close()

    
