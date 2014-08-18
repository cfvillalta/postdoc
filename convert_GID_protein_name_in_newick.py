#! /usr/bin/python

import sys
from Bio import Phylo
from subprocess import Popen, PIPE
import os
import re
###################################################################
#input fasta file and get rid of duplicates and print out new fasta
###################################################################
aligned_fasta_file = sys.argv[1]
aligned_fasta_file_split = aligned_fasta_file.split(".")

fasta = open(aligned_fasta_file, 'rU')

seqs = fasta.readlines()

seqs_dict = {}
id = ''
for line in seqs:
    if line.startswith('>'):
        id = line.strip()
        seqs_dict[id]=[]
    else:
        #   print id
        #print line
        seqs_dict[id].append(line.strip())

fasta_out = open("%s_no_dup.fasta" %(aligned_fasta_file_split[0]), 'w')
for seq in seqs_dict:
    fasta_out.write('%s\n' %(seq))
    fasta_out.write('%s\n' %('\n'.join(seqs_dict[seq])))

'''
#newick = sys.argv[1]

tree = Phylo.read(newick, 'newick')

#print tree

leafs= tree.get_terminals()

uniq_GID_name_dict = {}

for leaf in leafs:
    GID = leaf.name
    GID_split = GID.split("/")

    #print uniq_GID_name_dict
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    stdout = p.stdout.read()
    uniq_GID_name_dict[GID_split[0]] = stdout
    p.communicate()
    #print "%s\t%s" %(GID_split[0],stdout)

print 'done making dictionary of GID = taxID'

tree_text = open(newick, 'r')

lines = tree_text.readlines()
#for line in lines:
#   print line
#print lines[1]

for GID in uniq_GID_name_dict:
    ID = uniq_GID_name_dict[GID].strip()
    ID = ID.replace(' ', '_')  
    ID = ID.replace('[', '')
    ID = ID.replace(']', '')
    ID = ID.replace(',', '_')
    ID = ID.replace('/', '_')
    ID = ID.replace('__', '_')
    ID = ID.replace(':', '_')
    ID = ID.replace('\)', '_')
    ID = ID.replace('\(', '_')
    
    lines[0] = lines[0].replace(GID, ID)

tree_out = open('newick.out', 'w')
for line in lines:    
    tree_out.write('%s'%(line))
tree_out.close()

#import pylab
newick_mod = open('newick.out', 'rU')
tree_mod = Phylo.read('newick.out', 'newick')
tree_mod.ladderize()
Phylo.draw(tree_mod)
'''
