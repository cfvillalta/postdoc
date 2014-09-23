#!/usr/bin/env python

#input files and get a size of the seq and make box plots from it also output the quartiles and median. So I know where to make cutoffs.

import sys
import re

fasta_in = sys.argv[1]
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
## Custom x-axis labels
#ax.set_xticklabels(tyr_sorted)

#ax.set_xticklabels(tyr_sorted, rotation =90)
#ax.set_ylabel('radial growth in cm')
#ax.set_xlabel('tyroinase knockdowns grown in light or dark')
#ax = plt.gca()
#ax.set_autoscale_on(False)



boxplot_name = "testing.png"

array = np.array(boxplot_data)
print array
median = np.percentile(array, 50)
first_q = np.percentile(array, 25)
print first_q
print median
#plt.axis(ymin=0,ymax=10)
plt.boxplot(boxplot_data)
fig.savefig(boxplot_name)
#plt.show()


