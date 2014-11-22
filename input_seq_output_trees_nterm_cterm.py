#!/usr/bin/env python

#sequecnes will be input into script and the gid will be extracted, along with the begininning and end of the tyrosinase.
#for tyrosinases with multiple tyrosinase domains will just put the beginning and end of domains.
#will make 2 sets of trees, those that include seqs with multiple tyrosinase domains and those that do not.

import sys
import re
from Bio import Phylo
from subprocess import Popen, PIPE
import os
#get filepath of file input into script
fasta_file = sys.argv[1]
#split file path at . to separate path from extension
file_split = fasta_file.split(".")
#open file 
fasta = open(fasta_file,'rU')
#readlines in to list
seqs = fasta.readlines()
#make an empty dictionary, the dict will eventually have the GID as the key and a list as the value the list will have the start and end of the domain or string of domains, and the number of domains present.
seqs_dict = {}
#loop through seqs
for line in seqs:
    #make a regular expression object to look for the pattern below from the input fasta file. A fasta header and its coordinates
    gid = re.compile(r"(>)(\d+)(/)(\d+)\-(\d+)")
    #search for a match to the regex object above in the line.
    match = gid.search(line)
    #if there is a match
    if match:
        #get GID from regex object
        gid = match.group(2)
        #get start of domain from regex object
        start = match.group(4)
        #get end of domain position from regex object
        end = match.group(5)
        #if gid in dict run code below, the code below is to account for multiple domains because I want to know where the first domain begins and last domain ends.
        if gid in seqs_dict:
            #convert all strings to floating numbers, if the start is less than the start of a previous domain for the particular protein 
            if float(seqs_dict[gid][0]) < float(start):
                #convert all strings to floating numbers
                #if the end is greater than the end on record
                if float(seqs_dict[gid][1])> float(end):
#                  #overwrite current value for the key, include the new start,new ending, and add one to the number of domains.
                   seqs_dict[gid]=[seqs_dict[gid][0],seqs_dict[gid][1],seqs_dict[gid][2]+1]
                #else if the end is less than what is in the current value associated with the GID key
                else:
                   #overwrite the value associated with the key included in the new value include the new start position, the same end position, and add +1 to the number of domains. 
                   seqs_dict[gid]=[seqs_dict[gid][0],end,seqs_dict[gid][2]+1]
            #if the start is greater than the one listed for the gid
            else:
                #if end position is larger than the current position
                if float(seqs_dict[gid][1])> float(end):
                    #overwrite value for GID with same start, new end, add plus one for domain
                   seqs_dict[gid]=[start,seqs_dict[gid][1],seqs_dict[gid][2]+1]
                #if end position is less than the current one. 
                else:
                   #The value for GID will still be over written but the start and end will stay the same and the only change will be the +1 for number of domains.
                   seqs_dict[gid]=[start,end,seqs_dict[gid][2]+1]
        #if GID not in dict
        else:
            #n= number of domains which as far as we know the protein has at least one.
            n = 1
            #we input the GID key and its value into the dictionary, the value is a list with [start, end, n]
            seqs_dict[gid] = [start, end, n]
#md = multiple domains
#create a blank dictionary will put seqs with multiple and single domains in here
seqs_dict_md= {}
#sd = single domains
#create a blank dictionary and will put seqs with just single domains in here.
seqs_dict_sd = {}
#loop through seqs_dict
for gid in seqs_dict:
    #if only one domain
    if seqs_dict[gid][2] == 1:
        #add key and value pair to both the seqs_dict_sd and the seqs_dict_md dicts
        seqs_dict_sd[gid]= seqs_dict[gid]
        seqs_dict_md[gid]= seqs_dict[gid]
    #else if the seqs have more than one domain just add to the seqs_dict_md dictionary
    elif seqs_dict[gid][2] > 1:
        seqs_dict_md[gid]= seqs_dict[gid]


#STOPPED HERE

#first will work on seqs in multiple domain library. Then on the single domain.
#order in dict is: gid is key, start, end, # domains, nterm, cterm, taxid
seqs_dict_md_2 = {}
seqs_dict_sd_2 = {}

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
        seqs_dict_md_2[gid]= [seqs_dict_md[gid][0],seqs_dict_md[gid][1],seqs_dict_md[gid][2],nterm,cterm,stdout_split[0]]
#        seqs_dict_md[gid].append(nterm)
#        seqs_dict_md[gid].append(cterm)
#        seqs_dict_md[gid].append(stdout_split[0])
#        print gid
#        print stdout_split[1]
#        print nterm
#        print end 
#        print cterm
        if gid in seqs_dict_sd:
            nterm = stdout_split[1][0:int(start)-1]
            cterm = stdout_split[1][int(end):]
            seqs_dict_sd_2[gid]= [seqs_dict_sd[gid][0],seqs_dict_sd[gid][1],seqs_dict_sd[gid][2],nterm,cterm,stdout_split[0]]
 #           seqs_dict_sd[gid].append(nterm)
 #           seqs_dict_sd[gid].append(cterm)
 #           seqs_dict_sd[gid].append(stdout_split[0])
            #        print gid
            #        print stdout_split[1]
            #        print nterm
            #        print end 
            #        print cterm

    else:
        pass
#        del seqs_dict_md[gid]
#        if gid in seqs_dict_sd:
#            del seqs_dict_sd[gid]

#print seqs_dict_md
#print seqs_dict_sd

#outpout md and sd sequence files for nterm and cterm
fasta_nterm_md = open('%s_nterm_multiple_domains_unaligned.fasta'%(file_split[0]),'w')
fasta_cterm_md = open('%s_cterm_multiple_domains_unaligned.fasta'%(file_split[0]),'w')
fasta_nterm_sd = open('%s_nterm_single_domain_unaligned.fasta'%(file_split[0]),'w')
fasta_cterm_sd = open('%s_cterm_single_domain_unaligned.fasta'%(file_split[0]),'w')

for gid in seqs_dict_md_2:
    fasta_nterm_md.write(">%s\n%s\n" %(gid, seqs_dict_md_2[gid][3]))
    fasta_cterm_md.write(">%s\n%s\n" %(gid, seqs_dict_md_2[gid][4]))
    if gid in seqs_dict_sd_2:
        fasta_nterm_sd.write(">%s\n%s\n" %(gid, seqs_dict_sd_2[gid][3]))
        fasta_cterm_sd.write(">%s\n%s\n" %(gid, seqs_dict_sd_2[gid][4]))
fasta_nterm_md.close()
fasta_cterm_md.close()
fasta_nterm_sd.close()
fasta_cterm_sd.close()

#one issue with script if I have two results it considers it two domains. Still need to figure out a way to weed out duplicates. Maybe ask if domains overlap or something before I start looking at number of domains. 
#Found one instance where tyrosinase domains are the same just off by one domain and another instance where two domains are called but overlap maybe two domains that overlap or something.

#run with md seqs first
#clustalo
print 'begin clustalo_nterm_md'
print '%s_nterm_multiple_domains_unaligned.fasta' %(file_split[0])
clustalo_nterm_md = Popen(['time', 'clustalo', '-i', '%s_nterm_multiple_domains_unaligned.fasta' %(file_split[0]), '-o', '%s_nterm_multople_domains_aligned_clustalo.fa' %(file_split[0]), '--force'])
clustalo_nterm_md.communicate()
print 'done clustalo_nterm_md'


#run fasttree
print 'done with clustalo'
print 'Begin FastTreeMP'
FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s.log' %(aligned_fasta_file_split[0]), '%s_aligned_clustalo.fa' %(aligned_fasta_file_split[0])],stdout=PIPE)
newick_out = open("%s_clustalo.newick" %(aligned_fasta_file_split[0]), 'w')
newick_out.write(FastTreeMP.stdout.read())

FastTreeMP.communicate()
newick_out.close()
print 'Done with FastTreeMP'

