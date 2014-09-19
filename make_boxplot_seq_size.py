#!/usr/bin/env python

#input files and get a size of the seq and make box plots from it also output the quartiles and median. So I know where to make cutoffs.

import sys
import re

fasta_in = sys.argv[1]
fasta = open(fasta_in, 'rU')
seqs = fasta.readlines()

seqs_dict = {}

for line in seqs:
    line = line.strip()
    id = re.compile(r"(>)(\d+)") 
    match = id.search(line)
    if match:
        seq_id = match.group(2)
#        print seq_id
        seqs_dict[match.group(2)]=[]
 
    else:
#        print line
        seqs_dict[seq_id].append(line)


print seqs_dict

for seq in seqs_dict:
    length = len(seqs_dict[seq][0])
    print length
