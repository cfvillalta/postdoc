#!/usr/bin/python

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

fasta_out = open("%s.fasta" %(aligned_fasta_file_split[0]), 'w')
for seq in seqs_dict:
    fasta_out.write('%s\n' %(seq))
    fasta_out.write('%s\n' %('\n'.join(seqs_dict[seq])))
fasta_out.close()

###################################################################
#Input fasta file and run fasttree, out put is newick tree
###################################################################

print 'Starting FastTreeMP'
FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s.log' %(aligned_fasta_file_split[0]), '%s.fasta' %(aligned_fasta_file_split[0])],stdout=PIPE)
newick_out = open("%s.newick" %(aligned_fasta_file_split[0]), 'w')
newick_out.write(FastTreeMP.stdout.read())

FastTreeMP.communicate()
newick_out.close()
print 'Done with FastTreeMP'
###################################################################

#print '%s_no_dup.newick' %(aligned_fasta_file_split[0])

tree = Phylo.read('%s.newick' %(aligned_fasta_file_split[0]), 'newick')

#print tree

leafs= tree.get_terminals()

uniq_GID_name_dict = {}
print "Starting blastdbcmd searches"
x=0
for leaf in leafs:
    GID = leaf.name
    #print GID
    GID_split = GID.split("/")
    #print uniq_GID_name_dict
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    stdout = p.stdout.read()
    p.communicate()
    if stdout:
        x = x+1
        # print x
        new_ID ='_'.join([GID_split[0],stdout])
        uniq_GID_name_dict[x] = [GID_split[0],new_ID]
        # print new_ID
        
    else:
        x = x+1
        #        print x    
        # print "%s\t%s" %(GID_split[0].strip(),stdout)
        uniq_GID_name_dict[x]= [GID, '%s\n' %(GID)]
        #print "%s\t%s" %(x,uniq_GID_name_dict[x])

GID_tax = open('%s_GID_taxID.out' %(aligned_fasta_file_split[0]),'w')

for x in uniq_GID_name_dict:
    #print "%s\t%s" %(x,uniq_GID_name_dict[x])
    GID_tax.write('%s\t%s\t%s' %(x, uniq_GID_name_dict[x][0], uniq_GID_name_dict[x][1]))
    #print '%s\t%s\t%s' %(x, uniq_GID_name_dict[x][0], uniq_GID_name_dict[x][1])
print 'done making dictionary of GID = taxID'
GID_tax.close()

tree_text = open('%s.newick' %(aligned_fasta_file_split[0]), 'r')

GID_tax_in  = open('%s_GID_taxID.out' %(aligned_fasta_file_split[0]),'r')

GID_tax_input = GID_tax_in.readlines()

uniq_GID_name_dict2 ={}

num = 0
num_list = []
for GID_tax in GID_tax_input:
    #print x
    num=num+1
    num_list.append(num)
    GID_tax=GID_tax.strip()
    GID_tax_split = GID_tax.split("\t")
    # print x_split
    uniq_GID_name_dict2[GID_tax_split[0]]=[GID_tax_split[1],GID_tax_split[2]]

    #print uniq_GID_name_dict2

    
line = tree_text.read()
tree_text.close()
y=0
roof= 500
for GID in num_list:
    y=y+1
    GID = str(GID)
    if y<=roof:
        ID = uniq_GID_name_dict2[GID][1]
        #print ID
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
        #print ID
        print '%s\t%s_%s' %(y,GID,ID)
        line = line.replace(uniq_GID_name_dict2[GID][0], '%s' %(uniq_GID_name_dict2[GID][1]))
        print y
    elif y>roof:
        tree_out = open('%s_taxid_mod.newick' %(aligned_fasta_file_split[0]), 'w')
        tree_out.write('%s'%(line))
        tree_out.close()
        
        if (roof+500)<num:
            roof = roof+500
        else:
            roof = num
            print 'reached roof'
            print 'new roof = %s' %(roof)
print num            
print 'Done replacing IDs in newick'

