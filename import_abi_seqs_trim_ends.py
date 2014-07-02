#! /usr/bin/python


#will be a script where I input a batch of abi files and they are trimmed and out put as sequence files.x

import sys

from Bio import SeqIO

test_seq = sys.argv[1]

handle = open(test_seq, 'rb')
print handle

for record in SeqIO.AbiIO.AbiIterator(handle, trim = True):
    print record.seq

    output_handle = open("test.fasta", "w")
    SeqIO.write(record, output_handle, "fasta")
    output_handle.close()


