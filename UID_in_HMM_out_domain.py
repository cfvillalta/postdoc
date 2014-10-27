#!/usr/bin/env python 

import phylo_tools
import sys
import re
#list of UID
input = sys.argv[1]
input_2 = sys.argv[2]
#file with fasta seqs
input_s = input.split(".")

input_open =open(input, 'rU')

GIDs= input_open.readlines()

GID_list = []

for GID in GIDs:
    GID=GID.strip()
    GID_s=GID.split("/")
#    print GID_s[0]
    GID_list.append(GID_s[0])

input_2_open = open(input_2, 'rU')

seqs = input_2_open.readlines()
input_seqs ={} 
for seq in seqs:
    seq=seq.strip()
    if seq.startswith(">"):
        gid = re.compile(r"(>)(\d+)(/)")
        match= gid.search(seq)
        if match:
            id = match.group(2)
            input_seqs[id]=[]
    else:
        input_seqs[id].append(seq)

#print input_seqs

fasta = open('%s.fasta' %(input_s[0]),'w')
for seq in GID_list:
    if input_seqs[seq]:
        fasta.write('>%s\n%s\n' %(seq, ''.join(input_seqs[seq])))
    
phylo_tools.ClustalO(input_s[0])

phylo_tools.hmmbuild('%s_clustalo' %(input_s[0]))
