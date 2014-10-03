#!/usr/bin/env python

#input files and get a size of the seq and make box plots from it also output the quartiles and median. So I know where to make cutoffs.

import sys
import re

fasta_in = sys.argv[1]
fasta_in_split = fasta_in.split(".")
fasta = open(fasta_in, 'rU')
seqs = fasta.readlines()

seqs_dict = {}

for line in seqs:
    line = line.strip()
    id = re.compile(r"(>)(\d+)") 
    match = id.search(line)
    if match:
        seq_id = match.group(2)
#        print seq_id
        seqs_dict[match.group(2)]=[]
 
    else:
#        print line
        seqs_dict[seq_id].append(line)


#print seqs_dict
boxplot_data = []
for seq in seqs_dict:
    length = len(seqs_dict[seq][0])
#    print length
    seqs_dict[seq].append(length)
    boxplot_data.append(length)
#print seqs_dict

#going to make boxplot
#http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
import numpy as np
import matplotlib as mpl
import pylab

#mpl.use('agg')

import matplotlib.pyplot as plt

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)

num=0
tot = 0
boxplot_data_no_zero = []
for x in boxplot_data:
    tot = tot+1
    if x == 0:
       num=num +1 
    else:
       boxplot_data_no_zero.append(x)
       
print "seqs with 0 nterm %s" %(num)
print "total seqs %s" %(tot)

boxplot_name = "testing.png"

array = np.array(sorted(boxplot_data))
#print array
median = np.percentile(array, 50)
first_q = np.percentile(array, 25)
third_q =  np.percentile(array, 75)
IQR = third_q -first_q
lower_fence = first_q - (1.5*(IQR))
upper_fence = third_q + (1.5*(IQR))
print "first quartile = %s" %(first_q)
print "median = %s" %(median)
print "third quartile = %s" %(third_q)
print "IQR = %s" %(IQR)
print "lower fence = %s" %(lower_fence)
print "upper fence = %s" %(upper_fence)

group = []
group.extend(range(1,101))

for p in group: 
    num_1 = 0
    tot_1 = 0
    num_2 = 0
    percentile = np.percentile(array,p)
    for x in boxplot_data:
        tot_1 = tot_1+1
        if x < percentile:
            num_1=num_1 +1
        elif x > percentile:
            num_2 = num_2+1
    print "%s percentile is: %s seqs below this percentile = %s above percentile = %s" %(p,  np.percentile(array,p), num_1, num_2)

print tot_1

plt.boxplot(boxplot_data)
fig.savefig(boxplot_name)
plt.show(block=False)
boxplot_data = sorted(boxplot_data)
#print np.median(array)
#print boxplot_data[3202]
#print boxplot_data[3203]
#print boxplot_data[3204]
#print med

print "Save plot if you don't want it to close before entering percentile."
var = raw_input( "What percentile should I cut off at? (Insert a number no percentage sign, between 1-100)")

print "You entered %s" %(var)


seqs_above_per = {}
if (int(var) > 0) and (int(var) <= 100):
    print "number within range, will extract sequences above the %s percentile." %(var)
    for seq in seqs_dict:
        if int(seqs_dict[seq][1]) >= np.percentile(array,int(var)):
            seqs_above_per[seq] = seqs_dict[seq]
else:

    print "number not within range"

#print seqs_dict
    #print seqs_above_per


new_seq_file = open("%s_%s_percentile.fa" %(fasta_in_split[0],var),'w')
for seq in seqs_above_per:
    new_seq_file.write(">%s\n%s\n" %(seq, seqs_above_per[seq][0]))

new_seq_file.close()
    
import phylo_tools

#input just the main name without the fa.
phylo_tools.ClustalO("%s_%s_percentile" %(fasta_in_split[0],var))

#phylo_tools.FastTreeMP("%s_%s_percentile" %(fasta_in_split[0],var))



