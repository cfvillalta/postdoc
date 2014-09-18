#!/usr/bin/env python

#sequecnes will be input into script and the gid will be extracted, along with the begininning and end of the tyrosinase.
#for tyrosinases with multiple tyrosinase domains will just put the beginning and end of domains.
#will make 2 sets of trees, those that include seqs with multiple tyrosinase domains and those that do not.

import sys
import re
from Bio import Phylo
from subprocess import Popen, PIPE
import os

#input fasta file

fasta_file = sys.argv[1]
file_split = fasta_file.split(".")

fasta = open(fasta_file,'rU')

seqs = fasta.readlines()

seqs_dict = {}

for line in seqs:
#    print line.strip()
    gid = re.compile(r"(>)(\d+)(/)(\d+)\-(\d+)")
    match = gid.search(line)
    if match:
#        print line
#        print match.group(2)
        gid = match.group(2)
#        print match.group(4)
        start = match.group(4)
#        print match.group(5)
        end = match.group(5)
        
        if gid in seqs_dict:
           if float(seqs_dict[gid][0]) < float(start):
               if float(seqs_dict[gid][1])> float(end):
#                   print "%s\t%s\t%s\n" %(gid, seqs_dict[gid][0], end)
 #                  print line 
                   seqs_dict[gid]=[seqs_dict[gid][0],seqs_dict[gid][1],seqs_dict[gid][2]+1]
               else:
  #                 print "%s\t%s\t%s\n" %(gid,seqs_dict[gid][0],end)
   #                print line
                   seqs_dict[gid]=[seqs_dict[gid][0],end,seqs_dict[gid][2]+1]
           else:
               if float(seqs_dict[gid][1])> float(end):
    #               print "%s\t%s\t%s\n" %(gid, start, end)
     #              print line 
                   seqs_dict[gid]=[start,seqs_dict[gid][1],seqs_dict[gid][2]+1]
               else:
      #             print "%s\t%s\t%s\n" %(gid,start,end)
       #            print line
                   seqs_dict[gid]=[start,end,seqs_dict[gid][2]+1]
                   
                         
               
    
        else:
            #n= number of domains
            n = 1
            seqs_dict[gid] = [start, end, n]


#print seqs_dict

#md = multiple domains
seqs_dict_md= {}
#sd = single domains
seqs_dict_sd = {}

for gid in seqs_dict:
    if seqs_dict[gid][2] == 1:
        seqs_dict_sd[gid]= seqs_dict[gid]
        seqs_dict_md[gid]= seqs_dict[gid]
    elif seqs_dict[gid][2] > 1:
        seqs_dict_md[gid]= seqs_dict[gid]


#print 'multiple domains'
#print seqs_dict_md
#print 'single domains'
#print seqs_dict_sd

#first will work on seqs in multiple domain library. Then on the single domain.
#order in dict is: gid is key, start, end, # domains, full seq, nterm, cterm, taxid

for gid in seqs_dict_md:
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', gid, '-target_only','-outfmt', '%t\t%s'],stdout = PIPE)
    stdout = p.stdout.read()
    p.communicate()
    if stdout:
        stdout=stdout.strip()
        stdout_split = stdout.split("\t")
        start = seqs_dict_md[gid][0]
        end = seqs_dict_md[gid][1]
        #I did -1 because its one less since its python and its also one less because the start number is the start of the tyrosinase domain. Check by looking at output.
        nterm = stdout_split[1][0:int(start)-1]
        #cterm is just end because if I subtract 1 i get what end is.
        cterm = stdout_split[1][int(end):]
        seqs_dict_md[gid].append(nterm)
        seqs_dict_md[gid].append(cterm)
        seqs_dict_md[gid].append(stdout_split[0])
#        print gid
#        print stdout_split[1]
#        print nterm
#        print end 
#        print cterm
        if gid in seqs_dict_sd:
            nterm = stdout_split[1][0:int(start)-1]
            cterm = stdout_split[1][int(end):]
            seqs_dict_md[gid].append(nterm)
            seqs_dict_md[gid].append(cterm)
            seqs_dict_md[gid].append(stdout_split[0])
            #        print gid
            #        print stdout_split[1]
            #        print nterm
            #        print end 
            #        print cterm


    else:
        pass

print seqs_dict_md
print seqs_dict_md
