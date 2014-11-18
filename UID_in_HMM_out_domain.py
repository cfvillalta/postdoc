#!/usr/bin/env python 
#The purpose of this script was to put in a list of IDs from a phylogenetic tree branch and pull their sequecnes from a list of sequecnes I might have. The script then aligns those sequences with Clustal Omega and builds an HMM with the alignment.

import phylo_tools
import sys
import re

#list of UIDs, like a list of UIDs I had picked from java tree view
input = sys.argv[1]
#file with fasta seqs
input_2 = sys.argv[2]

#split file name at '.' to use name later
input_s = input.split(".")

#open list of UIDs
input_open =open(input, 'rU')

#read each line of IDs
GIDs= input_open.readlines()

#create list I will put IDs into.
GID_list = []

#for loop goes through GIDs list from text file.
for GID in GIDs:
#strip /n from each GID
    GID=GID.strip()
#split each GID by '/' because the GID is a number id, /, and coordinates of domain(in this case tyrosinase domains.)
    GID_s=GID.split("/")
#    print GID_s[0]
    GID_list.append(GID_s[0])
#inputs my txt file with fasta sequences.
input_2_open = open(input_2, 'rU')
#read each line of the text file into a list called seqs.
seqs = input_2_open.readlines()
#created an empty dict I will put seqs into with the seq id as the key and the value being the seqeucne.
input_seqs ={}
#loop through list seq. 
for seq in seqs:
#strip each string in list of trailign whitespace e.g. /n
    seq=seq.strip()
#strings in list that begin with ">"
    if seq.startswith(">"):
#within those will look for pattern of ">" followed by a number \d+ and ending with a backslash /. Search pattern is called gid
        gid = re.compile(r"(>)(\d+)(/)")
#search string for pattern in gid
        match= gid.search(seq)
#if match present
        if match:
#grab the id 
            id = match.group(2)
#use the id as the key for sequence in diction input_seqs
            input_seqs[id]=[]
#if no '>' then add to a list of seqs that belong to the id that superceded it.
    else:
        input_seqs[id].append(seq)

#make a file with the same name as the UID input file but with a .fasta file extenstion.
fasta = open('%s.fasta' %(input_s[0]),'w')
#Look through each key in the GID_list.
for seq in GID_list:
#if gid in dictionary 
    if input_seqs[seq]:
#write out the id and print joined seqs into new fasta file.
        fasta.write('>%s\n%s\n' %(seq, ''.join(input_seqs[seq])))
#align fasta file with clustal omega, outputs a clustal alignment    
phylo_tools.ClustalO(input_s[0])
#build hmm with clustal alignment using hmmbuild
phylo_tools.hmmbuild('%s_clustalo' %(input_s[0]))
