#!/usr/bin/python/

#in this script I want to input a file with fasta sequesnce that I am interested in and then pull the full sequences from NCBI. 

#After pulling sequences want to align them with muscle
#Build a phylogenetic tree with fast tree.
#convert to javatree view file formats.

import sys
import re
from Bio import Phylo
from subprocess import Popen, PIPE
import os

###################################################################
#input fasta file and get rid of some duplicates and output new 
#muscle aligned fasta.
###################################################################
aligned_fasta_file = sys.argv[1]
aligned_fasta_file_split = aligned_fasta_file.split(".")


fasta = open(aligned_fasta_file, 'rU')

seqs = fasta.readlines()

seqs_dict = {}
id = ''
print 'Get Full Seqs'
for line in seqs:

    if line.startswith('>'):
        gid = re.compile(r"(>)(\d+)(/)")
#        print line
        match = gid.search(line)
        if match:
            id = match.group(2)
            p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', id, '-target_only','-outfmt', '%t\t%s'],stdout = PIPE)
            stdout = p.stdout.read()
            p.communicate()
            if stdout:
                stdout_split = stdout.split("\t")
                seqs_dict[id]= stdout_split
            else:
                pass
        else:
            pass
    else:
        pass
#made this because I might use taxID later but dont want the name to get cut in the muscle alignment or fastree.

#print seqs_dict

fasta = open('%s_unaligned.fa' %(aligned_fasta_file_split[0]), 'w')
for seq in seqs_dict:
    fasta.write('>%s\n%s' %(seq,seqs_dict[seq][1]))

fasta.close()
          
#run muscle
print 'Done getting Full Seqs'
#print 'Begin Muscle'
#muscle = Popen(['time','muscle3.8.31_i86darwin64', '-in', '%s_unaligned.fa' %(aligned_fasta_file_split[0]), '-out', '%s_aligned.fa' %(aligned_fasta_file_split[0])])
#muscle.communicate()
#print 'Done with muscle'

#no longer running muscle saw that clustalo is faster and more accurate. 

#clustalo_multithread
#clustalo = Popen(['time', 'clustalo', '-i', '%s_unaligned.fa' %(aligned_fasta_file_split[0]), '-o', '%s_aligned.fa' %(aligned_fasta_file_split[0]), '--force', '--threads=4']) 
#clustalo
print 'begin clustalo'
clustalo = Popen(['time', 'clustalo', '-i', '%s_unaligned.fa' %(aligned_fasta_file_split[0]), '-o', '%s_aligned_clustalo.fa' %(aligned_fasta_file_split[0]), '--force'])
clustalo.communicate()
print clustalo
#run fasttree
print 'done with clustalo'
print 'Begin FastTreeMP'

FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s.log' %(aligned_fasta_file_split[0]), '%s_aligned.fa' %(aligned_fasta_file_split[0])],stdout=PIPE)
newick_out = open("%s.newick" %(aligned_fasta_file_split[0]), 'w')
newick_out.write(FastTreeMP.stdout.read())

FastTreeMP.communicate()
newick_out.close()
print 'Done with FastTreeMP'


