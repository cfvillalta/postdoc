#!/usr/bin/env python 
#program just accepts a UID sequence and then outputs the full fasta sequence.
import phylo_tools
import sys
#inout a list of GIDS with one GID per line.
input = sys.argv[1]
#split file name from extenstion.
input_s = input.split(".")
#open file
input_open =open(input, 'rU')
#read each line of file into a list with each line a string in the list.
GIDs= input_open.readlines()
#list I will put GIDs into
GID_list = []
#loop through GID list
for GID in GIDs:
#strip /n from string
    GID=GID.strip()
#split string at "/"
    GID_s=GID.split("/")
#    print GID_s[0]
#add GID to new list GID_list
    GID_list.append(GID_s[0])
#get seqs from ncbi NR using blastdbcmd. Output is a dictionary
fasta_seqs = phylo_tools.GID2seq(GID_list)

#print fasta_seqs
#open new text file with fasta extension
fasta = open('%s.fasta' %(input_s[0]),'w')
#loop through fasta_seqs
for seq in fasta_seqs:
#write each seq in dictionary into opened fasta file in fasta format.
    fasta.write('>%s\n%s' %(seq, fasta_seqs[seq][1]))
    
