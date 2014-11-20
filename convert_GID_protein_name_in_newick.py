#!/usr/bin/python
#import packages and modules I will be using in the script
import sys
from Bio import Phylo
from subprocess import Popen, PIPE
import os
import re
###################################################################
#input fasta file and get rid of duplicates and print out new fasta
###################################################################
#get filepath of aligned fasta file
aligned_fasta_file = sys.argv[1]
#split file path name from extension
aligned_fasta_file_split = aligned_fasta_file.split(".")
#open alignment file
fasta = open(aligned_fasta_file, 'rU')
#read lines into list called seqs
seqs = fasta.readlines()
#make an empty dictionary called seqs_dict
seqs_dict = {}
#make an empty string called id
id = ''
#loop through each line of seqs
for line in seqs:
    #if line starts with '>' its the fasta header
    if line.startswith('>'):
        #strip white space from id
        id = line.strip()
        #i did this step to get rid of seqs with the same GID since a dictionary will overwrite the same key.
        #use id as key in seqs_dict with empty list as value
        seqs_dict[id]=[]
    #else if not fasta header run code below.
    else:
        #if not fasta header its sequence infor and line is striped of whitespace and appended to list that is value in seqs dict.
        seqs_dict[id].append(line.strip())
#open a new fasta file with the same name as the aligned file but with a .fasta extension
fasta_out = open("%s.fasta" %(aligned_fasta_file_split[0]), 'w')
#loop through seqs_dict
for seq in seqs_dict:
    #write seq key to fasta file, it will be the fasta seq header.
    fasta_out.write('%s\n' %(seq))
    #join seqs in list for the value in the dictionary corresponding to the key above and print out the sequence below the corresponding fasta header.
    fasta_out.write('%s\n' %('\n'.join(seqs_dict[seq])))
#close fasta file.
fasta_out.close()

###################################################################
#Input fasta file and run fasttree, out put is newick tree
###################################################################
#tells using FastTreeMP MP= multiprocessor is going to start.
print 'Starting FastTreeMP'
#subprocess to run FastTreeMP within python. FastTreeMP will run the fasta created above and will PIPE the output which is a newick tree to stdout
FastTreeMP = Popen(['FastTreeMP', '-quiet', '-nopr', '-log', '%s.log' %(aligned_fasta_file_split[0]), '%s.fasta' %(aligned_fasta_file_split[0])],stdout=PIPE)
#open a new newick file that I will write newick formatted data into, will have the same file name as the input file but with a .newick extension.
newick_out = open("%s.newick" %(aligned_fasta_file_split[0]), 'w')
#write the output from the FastTreeMP subprocess into the new newick file.
newick_out.write(FastTreeMP.stdout.read())
#command that tells the script to wait until the subprocess is done before it can continue.
FastTreeMP.communicate()
#close the newick file because all writing is done.
newick_out.close()
#tells user fasttreeMP is done.
print 'Done with FastTreeMP'
###################################################################
#use the phylo module from the biopython package to read in tree data from the newick file created above.
tree = Phylo.read('%s.newick' %(aligned_fasta_file_split[0]), 'newick')
#extract all the IDs for all terminal portions of the tree, so basically the IDs of sequences used to build the tree.
leafs= tree.get_terminals()
#make an empty dictionary I will put GIDs into as the key and taxonomic information for the id into as the value.
uniq_GID_name_dict = {}
#telling the user I am going to begin using blastdbcmd to search for taxonomic info of each GID present in the tree.
print "Starting blastdbcmd searches"
#made a counter set to zero (integer variable)
x=0
#loop through list leafs
for leaf in leafs:
    #extract the gid from leaf variable
    GID = leaf.name
    #split the GID string in order to just get the id itself
    GID_split = GID.split("/")
    #run subprocess p. The subprocess is just running blastdbcmd, where the GID is input and the output is taxonomic information (genus and species name for the sequence, information is piped to stdout)
    p = Popen(['blastdbcmd', '-db', 'nr', '-dbtype', 'prot', '-entry', GID_split[0], '-target_only','-outfmt', '%t'],stdout = PIPE)
    #read the stdout, which has the taxonomic information.
    stdout = p.stdout.read()
    #wait for script to finish before proceeding.
    p.communicate()
    #if there is a std out run code below
    if stdout:
        #add one to counter
        x = x+1
        #make a new id which is the GID joined to the stdout with a underscore. 
        new_ID ='_'.join([GID_split[0],stdout])
        #use the number from the x counter as the key and have a list as a value. The list contains the GID and the new id.
        uniq_GID_name_dict[x] = [GID_split[0],new_ID]
    #if no stdout
    else:
        #add one to the counter
        x = x+1
        #use the number from the counter as the key and as the value input the GID twice.
        uniq_GID_name_dict[x]= [GID, '%s\n' %(GID)]
#open new file to output GID and taxid. I think I made a file just to have the data handy in a text file for later use. But I could do something different than this step.
GID_tax = open('%s_GID_taxID.out' %(aligned_fasta_file_split[0]),'w')
#STOPPED HERE
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

