#! /usr/bin/python
#This script converts a fasta formatted sequence file to stockholm format using alignIO from the Biopython package.

import sys

#Get filepath to stockholm formatted alignment.
stockholm_file = sys.argv[1]
#split file path before the extension.
file_name_split = stockholm_file.split(".")

from Bio import AlignIO
#open the stockholm file.
input_stockholm = open(stockholm_file, "rU")
#make a new file with a fasta extension to input fasta data into below.
output_fasta = open("%s.fasta" %(file_name_split[0]), "w")
#parse out stockholm sequence data with alignio.parse into alignment list
alignment = AlignIO.parse(input_stockholm, "stockholm")
#use alignio.write to wrtie alignment data into the opened fasta file in fasta format.
AlignIO.write(alignment, output_fasta, "fasta")
#close fasta file.
output_fasta.close()
#close stockholm file
input_stockholm.close()
