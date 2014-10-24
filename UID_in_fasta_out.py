#!/usr/bin/env python 

import phylo_tools
import sys

input = sys.argv[1]
input_s = input.split(".")

input_open =open(input, 'rU')

GIDs= input_open.readlines()

GID_list = []

for GID in GIDs:
    GID=GID.strip()
    GID_s=GID.split("/")
#    print GID_s[0]
    GID_list.append(GID_s[0])

fasta_seqs = phylo_tools.GID2seq(GID_list)

#print fasta_seqs

fasta = open('%s.fasta' %(input_s[0]),'w')
for seq in fasta_seqs:
    fasta.write('>%s\n%s' %(seq, fasta_seqs[seq][1]))
    
