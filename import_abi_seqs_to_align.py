#! /usr/bin/python


from abi_seq_tools import trim
import sys
import re

directory_name = sys.argv[1]
seq_info = sys.argv[2]

fh = open(seq_info, 'rb')

print directory_name

seqs = trim(directory_name)

#print seqs

#print seq_info

#print fh
file = fh.readlines() 
#print file

samples = {}

for line in file:
    lines = line.split('\r')
    #print lines

    for sample in lines:
        x = sample.split('\t')
        reObj =  re.compile(x[0])
        #print reObj
        for key in seqs.keys():
            
            
            if(reObj.search(key)):
            #print key, x[0]
            #  print x
            #  print seqs[key].seq
               
               if x[2] == 'FOR':
                   #                   sequence = seqs[key].
                   x.append(seqs[key].seq)
                   samples[x[0]]= x
               elif x[2] == 'REV':
                   #print x
                   #print seqs[key].seq
                   #print seqs[key].seq.reverse_complement()
                   x.append(seqs[key].seq.reverse_complement())
                   samples[x[0]]= x

        

                   #print samples['CV190'][4]
               #print seqs


        
