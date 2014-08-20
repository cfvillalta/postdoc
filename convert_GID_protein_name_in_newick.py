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
fasta_out.close()
###################################################################
#Input fasta file and run fasttree, out put is newick tree
###################################################################
print 'Starting FastTreeMP'
FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s_no_dup.log' %(aligned_fasta_file_split[0]), '%s_no_dup.fasta' %(aligned_fasta_file_split[0])],stdout=PIPE)
newick_out = open("%s_no_dup.newick" %(aligned_fasta_file_split[0]), 'w')
newick_out.write(FastTreeMP.stdout.read())

FastTreeMP.communicate()
newick_out.close()
print 'Done with FastTreeMP'
###################################################################

#print '%s_no_dup.newick' %(aligned_fasta_file_split[0])

tree = Phylo.read('%s_no_dup.newick' %(aligned_fasta_file_split[0]), 'newick')

#print tree

leafs= tree.get_terminals()

uniq_GID_name_dict = {}
print "Starting blastdbcmd searches"
for leaf in leafs:
    GID = leaf.name
    GID_split = GID.split("/")
    #print uniq_GID_name_dict
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    stdout = p.stdout.read()
    p.communicate()
    if stdout:
        uniq_GID_name_dict[GID_split[0]] = stdout
    else:    
        print "%s\t%s" %(GID_split[0],stdout)
        uniq_GID_name_dict[GID_split[0]]=GID_split[0]
print 'done making dictionary of GID = taxID'

tree_text = open('%s_no_dup.newick' %(aligned_fasta_file_split[0]), 'r')

line = tree_text.read()
tree_text.close()

for GID in uniq_GID_name_dict:
    ID = uniq_GID_name_dict[GID].strip()
    print ID
    ID = ID.replace(' ', '_')  
    ID = ID.replace('[', '')
    ID = ID.replace(']', '')
    ID = ID.replace(',', '_')
    ID = ID.replace('/', '_')
    ID = ID.replace('__', '_')
    ID = ID.replace(':', '_')
    ID = ID.replace('.', '_')
    ID = ID.replace('(', '_')
    ID = ID.replace(')', '_')
    ID = ID.replace(';', '_')
    ID = ID.replace('+', '_')
    ID = ID.replace('=', '_')
    ID = ID.replace('__', '_')
    ID = ID.replace('__', '_')
    ID = ID.replace('__', '_')
    print ID
    print '%s_%s' %(GID,ID)
    line = line.replace(GID, '%s_%s' %(GID,ID))
print 'Done replacing IDs in newick'

tree_out = open('%s_no_dup_align_tax.newick' %(aligned_fasta_file_split[0]), 'w')
   
tree_out.write('%s'%(line))
tree_out.close()

#This part does not work cannot get it into phylopython.
'''
tree_mod = Phylo.read('%s_no_dup_align_tax.newick' %(aligned_fasta_file_split[0]),'newick')
newick_mod.close()
tree_mod.ladderize()
Phylo.draw(tree_mod)
'''
