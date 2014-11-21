#!/usr/bin/python/

#in this script I want to input a file with fasta sequesnce that I am interested in and then pull the full sequences from NCBI. 
#After pulling sequences want to align them with clustalo, originally used muscle but clustalo works better in comparison.
#Build a phylogenetic tree with FastTreeMP.
#convert to javatree view file formats.
#several sections of this script have since making this script become classes in my wikitools module
import sys
import re
from Bio import Phylo
from subprocess import Popen, PIPE
import os

###################################################################
#input fasta file and get rid of some duplicates and output new 
#muscle aligned fasta.
###################################################################
#get file path of fasta file
aligned_fasta_file = sys.argv[1]
#split filepath from extension
aligned_fasta_file_split = aligned_fasta_file.split(".")
#open fasta file in python
fasta = open(aligned_fasta_file, 'rU')
#read lines into list.
seqs = fasta.readlines()
#make an empty dictionary
seqs_dict = {}
#make an empty string
id = ''
#print get full seqs to tell user what we are doing.
print 'Get Full Seqs'
#loop through the seqs list
for line in seqs:
    #if list starts with a fasta header >
    if line.startswith('>'):
        #search for the pattern below of >number/
        gid = re.compile(r"(>)(\d+)(/)")
        #search for match in line
        match = gid.search(line)
        #if there is a match
        if match:
            #grab the (\d+) portion from the search and call it id.
            id = match.group(2)
            #run blastdbcmd subprocess to get taxonomic and full seq, instead of just domain seq, information and PIPE it out as stdout.
            p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', id, '-target_only','-outfmt', '%t\t%s'],stdout = PIPE)
            #read stdout from subprocess into stdout string.
            stdout = p.stdout.read()
            #wait until subprocess is done to move on
            p.communicate()
            #if there is a stdout
            if stdout:
                #split the stdout at tabs into a list stdout_split
                stdout_split = stdout.split("\t")
                #use the id as the key to dictionary called seqs_dict and the stdout_split list  as the value
                seqs_dict[id]= stdout_split
            #if there was no stdout pass and move onto next line
            else:
                pass
        #if there was no match pass onto next line
        else:
            pass
    #if line does not start with > aka fasta header move onto next line.
    else:
        pass
#made this because I might use taxID later but dont want the name to get cut in the muscle alignment or fastree.
#open new fasta file to stick full fasta seqs into.
fasta = open('%s_unaligned.fa' %(aligned_fasta_file_split[0]), 'w')
#loop through seqs_dict
for seq in seqs_dict:
    #write GID and full sequence in fasta format into the new file above
    fasta.write('>%s\n%s' %(seq,seqs_dict[seq][1]))
#close fasta file.
fasta.close()
#tell the user we are done getting full seqs from the nr database.          
print 'Done getting Full Seqs' 
#tell user we are beginning clustalo
print 'begin clustalo'
#open subprocess to run clustalo in order to align the newly created fasta file with full sequences. An aligned seqeucne file is produced in clustal and its named with the same filepath as the original unaligned file but with the addition of _aligned_clustalo.fa
clustalo = Popen(['time', 'clustalo', '-i', '%s_unaligned.fa' %(aligned_fasta_file_split[0]), '-o', '%s_aligned_clustalo.fa' %(aligned_fasta_file_split[0]), '--force'])
#wait until subprocess is done before continuing
clustalo.communicate()
#tells user clustalo is done running
print 'done with clustalo'
#tells user we are going to run FastTreeMP
print 'Begin FastTreeMP'
#run FastTreeMP as a subprocess in python. Build a tree using the aligned sequence file that was output from clustalo. 
FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s.log' %(aligned_fasta_file_split[0]), '%s_aligned_clustalo.fa' %(aligned_fasta_file_split[0])],stdout=PIPE)
#open a new textfile where we will input newick tree file data.
#wait until FastTreeMP is done
FastTreeMP.communicate()
newick_out = open("%s_clustalo.newick" %(aligned_fasta_file_split[0]), 'w')
#write stdout that was piped out of the FastTreeMP subprocess into the newick file.
newick_out.write(FastTreeMP.stdout.read())
#close newick file.
newick_out.close()
#let user know we are done with FastTreeMP
print 'Done with FastTreeMP'


