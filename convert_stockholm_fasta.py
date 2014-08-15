#! /usr/bin/python


import sys

#input a stockholm formatted alignment.
stockholm_file = sys.argv[1]

file_name_split = stockholm_file.split(".")

print file_name_split


#import AlignIO from Bio python
from Bio import AlignIO

input_stockholm = open(stockholm_file, "rU")
output_fasta = open("%s.fasta" %(file_name_split[0]), "w")


alignment = AlignIO.parse(input_stockholm, "stockholm")
AlignIO.write(alignment, output_fasta, "fasta")

output_fasta.close()
input_stockholm.close()
