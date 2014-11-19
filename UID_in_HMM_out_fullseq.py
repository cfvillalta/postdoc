#!/usr/bin/env python 
#script is similar to the script I made to build an hmm from the domain seqs of specific list of sequence IDs. This script is shorter because I dont need a second file with domain sequecnes handy and can just pull sequences from NCBI nr database.
import phylo_tools
import sys

#input file with GIDs
input = sys.argv[1]
#split file name and extension by '.'
input_s = input.split(".")
#open file
input_open =open(input, 'rU')
#read lines into a list where each line is a string.
GIDs= input_open.readlines()
#list I will put each GID into.
GID_list = []
#loop through GIDs
for GID in GIDs:
#strip GID of /n
    GID=GID.strip()
#split by "/" to get just GID and not length coordinates
    GID_s=GID.split("/")
#    print GID_s[0]
#add GID to GID_list
    GID_list.append(GID_s[0])
#input GID list into my phylo tools module that that takes in a list of GIDs and outputs a dictionary with GID as the key and sequence as the values. Gets seq using nr database search with blastdbcmd from the blast package.
fasta_seqs = phylo_tools.GID2seq(GID_list)

#print fasta_seqs
#open a new text file wiht fasta extension I will put seqs into in fasta format.
fasta = open('%s.fasta' %(input_s[0]),'w')
#loop through fasta_seqs dict
for seq in fasta_seqs:
#write seqs to opened file in fasta format. 
    fasta.write('>%s\n%s' %(seq, fasta_seqs[seq][1]))
#align fasta seqs with clustal omega    
phylo_tools.ClustalO(input_s[0])
#build an hmm of the seqs from the clustal alignment.
phylo_tools.hmmbuild('%s_clustalo' %(input_s[0]))
