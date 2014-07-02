#! /usr/bin/python

def trim(input_directory_here):
#will be a script where I input a batch of abi files and they are trimmed and out put as sequence files.x

    import sys
    import os

    from Bio import SeqIO

    seq_dir = input_directory_here

    seqs = {}

    for file in os.listdir(seq_dir):
        if file.endswith(".ab1"):
            file_path = "%s%s" %(seq_dir,file)
        
            handle = open(file_path, 'rb')



            for record in SeqIO.AbiIO.AbiIterator(handle, trim = True):
                #print record.id
                #print 
                #print record
                
                seqs[record.id] = record
    
            # output_handle = open("test.fasta", "w")
            # SeqIO.write(record, output_handle, "fasta")
            #output_handle.close()

    return(seqs)
