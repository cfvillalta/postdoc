#! /usr/bin/python
#in this script I was converting my fasta alignment file into a clustal alignment file. Using AlignIO from Biopython

import sys

#get filepath for fasta formatted alignment.
fasta_file = sys.argv[1]
#split file path at . from extension
file_name_split = fasta_file.split(".")

from Bio import AlignIO
#open fasta file
input_fasta = open(fasta_file, "rU")
#open a new clustal file and use the file path without extension to name it with the new .aln extension
output_clustal = open("%s.aln" %(file_name_split[0]), "w")
#use AlignIO.parse to read in fasta file and name the read in data alignment.
alignment = AlignIO.parse(input_fasta, "fasta")
#use alignIO.write to output alignment data as clustal format into the opened file 'output_clustal'.
AlignIO.write(alignment, output_clustal, "clustal")
#close output_clustal because we are done.
output_clustal.close()
#close input_fasta file as well since we are done accessing data from the file.
input_fasta.close()
