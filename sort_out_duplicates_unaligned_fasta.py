#!/usr/bin/env python

import sys


fa_in = sys.argv[1]

fa_in_split = fa_in.split(".")

fa_open = open(fa_in, 'rU')

fa = fa_open.readlines()

#print fa

fa_seq_key = {}

fa_id_key = {}
                
for seq in fa:
    seq=seq.strip()
    if seq.startswith('>'):
        id = seq
        fa_id_key[id] = []
    else:
        fa_id_key[id].append(seq)

        #print fa_id_key

for id in fa_id_key:
    seq = ''.join(fa_id_key[id])
    fa_seq_key[seq] = id

    #print fa_seq_key


fa_out = open('%s_no_dups.fa' %(fa_in_split[0]), 'w')

for seq in fa_seq_key:
    fa_out.write('%s\n' %(fa_seq_key[seq]))
    fa_out.write('%s\n' %(seq))
