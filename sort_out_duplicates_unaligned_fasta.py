#!/usr/bin/env python
#Script was built to try and get rid of some duplicate sequences by having the GID be the key and having any duplicate keys when inserted into the dictionary overwriting the previous key. Does not get rid of duplicates but gets rid of some. I also wanted to get rid of duplicated by sequence incase the GIDs were different and the sequences were the same.BUt it created problems with getting rid of some ids I wanted to keep.
import sys
#open filepath to fasta file input by user.
fa_in = sys.argv[1]
#split filepath before extension at "."
fa_in_split = fa_in.split(".")
#open file
fa_open = open(fa_in, 'rU')
#read lines into list called fa
fa = fa_open.readlines()
#open blank dictionary,where the sequence will be the key and the id the value.
fa_seq_key = {}
#open a blank dictionary where I will put the id as the key and the sequence as the value
fa_id_key = {}
#loop though fa list.                
for seq in fa:
    #for each seq strip whitespace.
    seq=seq.strip()
    #if seq starts with > it is the fasta header.
    if seq.startswith('>'):
        #copy seq to id
        id = seq
        #use the id as the key for fa_id_key
        fa_id_key[id] = []
    #not id with > 
    else:
        #append string to list in value.
        fa_id_key[id].append(seq)

#loop throught the dictionary fa_id_key
for id in fa_id_key:
    #join values for each id into one large sequence.
    seq = ''.join(fa_id_key[id])
    #overwrite previous value with new value.
    fa_id_key[id] = seq
#open a new file to write fasta seqs. 
fa_out = open('%s_no_dups.fa' %(fa_in_split[0]), 'w')
#loop through fa_id_key
for seq in fa_id_key:
    #for each seq write out seqid in fasta format
    fa_out.write('%s\n' %(seq))
    #write out sequence in fasta format after seq_id
    fa_out.write('%s\n' %(fa_id_key[seq]))
#close fa_out after done writing seqs to file.
fa_out.close()
