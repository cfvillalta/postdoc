#! /usr/bin/python

import sys
from Bio import Phylo

newick = sys.argv[1]

tree = Phylo.read (newick, 'newick')

#print tree

leafs= tree.get_terminals()

for leaf in leafs:
    GID = leaf.name
    GID_split = GID.split("/")
    print GID_split[0]
