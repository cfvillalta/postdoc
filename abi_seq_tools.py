#! /usr/bin/python
#module with classes to help in analyzing abi seqs.

#class  is used to trim abi seqs of degenerate low quality sequence  using SeqIO.AbiIterator.
#input a directory into class full of abi seqs.
def trim(input_directory_here):
#will be a script where I input a batch of abi files and they are trimmed and out put as sequence files.x

    import sys
    import os

    from Bio import SeqIO
#call directory seq_dir
    seq_dir = input_directory_here
#make a dictionary called seqs.
    seqs = {}
#use os.listdir to make seq_dir into a list of files in dir and loop through it.
    for file in os.listdir(seq_dir):
#if file ends with .ab1
        if file.endswith(".ab1"):
#put together the name of the file path in order to open the actual file in the folder.
            file_path = "%s%s" %(seq_dir,file)
#open .ab1 file from above
            handle = open(file_path, 'rb')


#go through abi and trim
            for record in SeqIO.AbiIO.AbiIterator(handle, trim = True):             
#add seq id as key and sequence as value.
                seqs[record.id] = record
#return dictionary.
    return(seqs)
