#! /usr/bin/python


import sys

#input a fasta formatted alignment.
fasta_file = sys.argv[1]

file_name_split = fasta_file.split(".")

print file_name_split


#import AlignIO from Bio python
from Bio import AlignIO

input_fasta = open(fasta_file, "rU")
output_clustal = open("%s.aln" %(file_name_split[0]), "w")


alignment = AlignIO.parse(input_fasta, "fasta")
AlignIO.write(alignment, output_clustal, "clustal")

output_clustal.close()
input_fasta.close()
