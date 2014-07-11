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

#Need to input scaffold sequences. In this first case its pDG71_TYR1-TYR7 and vector, so 8 sequcnes. Will be in fasta format.
import os
from Bio import SeqIO
from Bio import Alphabet
from Bio import Seq
from Bio.Alphabet import IUPAC
from Bio.Align import AlignInfo
from Bio.Align.Generic import Alignment
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

scaffold_seqs =  sys.argv[3]

scaffolds = {}

for file in os.listdir(scaffold_seqs):
            file_path = "%s%s" %(scaffold_seqs,file)
        
            handle = open(file_path, 'rU')

            for record in SeqIO.parse(handle, 'fasta'):
                #print record.id
                scaffolds[record.name] = record

                #print scaffolds
seq_groups ={}
                
for sample in samples:
    #print samples[sample][3]
    reObj = re.compile(samples[sample][3])
    for key in scaffolds:
        if(reObj.search(key)):
        #print key, samples[sample]
            seq_groups[samples[sample][3]] = [scaffolds[key]]
            

for sample in samples:
    #print samples[sample][3]
    reObj = re.compile(samples[sample][3])
    for key in scaffolds:
        if(reObj.search(key)):
        #print key, samples[sample]
            
            seq_groups[samples[sample][3]].extend([samples[sample]])
                        
for group in seq_groups:
    
    for x in seq_groups[group]:
        try:
            file= open(('%s_%s.fasta')%(group, x.id),'w')
            clustal_input = ''
            clustal_input+=('>%s_%s\n'%(group, x.id))
            clustal_input+=('%s\n'%(str(x.seq)))
            file.write(clustal_input)
            file.close()
        except:
            clustal_input = ''
            file= open(('%s_%s.fasta')%(group, x[0]),'w')
            clustal_input+=('>%s_%s\n'%(group, x[0]))
            clustal_input+=('%s\n'%(str(x[4])))
            file.write('%s/%s' %(directory_name,clustal_input))
            file.close()


            #alignment = MultipleSeqAlignment(Alphabet.Gapped(IUPAC.unambiguous_dna))
            
            #print clustal_input
