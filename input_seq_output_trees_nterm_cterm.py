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

seqs_dict= {}

for line in seqs:
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
