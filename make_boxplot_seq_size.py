#!/usr/bin/env python

#input files and get a size of the seq and make box plots from it also output the quartiles and median. So I know where to make cutoffs. The script was created because i was having and issue with the nterm seqs and wanted to know their size distribution, because some proteins have no nterm seqs or they are very small. 
import sys
import re
#get filepath 
fasta_in = sys.argv[1]
#split file path from file extension portion
fasta_in_split = fasta_in.split(".")
#open fasta file in python.
fasta = open(fasta_in, 'rU')
#read lines into list called seqs.
seqs = fasta.readlines()
#create empty dictionary called seqs dict. Will use GID as key and sequence as the value.
seqs_dict = {}
#loop through lines in seqs.
for line in seqs:
    #strip whitespace from line
    line = line.strip()
    #compile search object for regex to search for fasta header.
    id = re.compile(r"(>)(\d+)")
    #determine if there is a match to regex object aka fasta header.
    match = id.search(line)
    #if a match is present.
    if match:
        #get GID from header
        seq_id = match.group(2)
        #add GID as key to seqs_dict
        seqs_dict[match.group(2)]=[]
    #no match to regex object, must be fasta sequence.
    else:
        #add sequence to list in value for the last GID used.
        seqs_dict[seq_id].append(line)
#make a blank list called boxplot_data
boxplot_data = []
#loop through seqs_dict
for seq in seqs_dict:
    #get length of seq for the corresponding GID
    length = len(seqs_dict[seq][0])
    #add length to list/value in dictionary.
    seqs_dict[seq].append(length)
    #add length to boxplot data.
    boxplot_data.append(length)
#going to make boxplot
#http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
import numpy as np
import matplotlib as mpl
import pylab
import matplotlib.pyplot as plt

#make figure
fig = plt.figure(1, figsize=(9, 6))
#add plot to figure.
ax = fig.add_subplot(111)
#make a number counter set to zero
num=0
#make a second counter set to zero
tot = 0
#make an empty list called boxplot_data_no_zero
boxplot_data_no_zero = []
#loop through boxplot_data
for x in boxplot_data:
    #add one for every x
    tot = tot+1
    #if x is equal to zero
    if x == 0:
        #add one to num counter
        num=num +1 
    #x is more than zero. Add to boxplot_data_no_zero list.
    else:
       boxplot_data_no_zero.append(x)
#print the number of seqs with no nterm       
print "seqs with 0 nterm %s" %(num)
#print the number of total seqs.
print "total seqs %s" %(tot)
#name the file I will output boxplot into.
boxplot_name = "testing.png"
#sort boxplot_data numbers and input into a numpy array.
array = np.array(sorted(boxplot_data))
#get the median
median = np.percentile(array, 50)
#get the first quartile
first_q = np.percentile(array, 25)
#get the third quartile.
third_q =  np.percentile(array, 75)
#get the interquartile range
IQR = third_q -first_q
#get the lower fence anything outside of that is an outlier
lower_fence = first_q - (1.5*(IQR))
#get the upper fence anything above that is an outsider.
upper_fence = third_q + (1.5*(IQR))
#print out first quartile
print "first quartile = %s" %(first_q)
#print median
print "median = %s" %(median)
#print third quartile
print "third quartile = %s" %(third_q)
#print interquartile range
print "IQR = %s" %(IQR)
#print lower fence
print "lower fence = %s" %(lower_fence)
#print upper fence
print "upper fence = %s" %(upper_fence)
#make an empty list called group.
group = []
#fill the group up with numbers that range from 1-101, basically 1-100.
group.extend(range(1,101))
#loop through group list
for p in group:
    #will have three counters all set to zero.
    num_1 = 0
    tot_1 = 0
    num_2 = 0
    #p from the group list will be used to determine what number in the array is at the specific p percentile.
    percentile = np.percentile(array,p)
    #loop through boxplot_data
    for x in boxplot_data:
        #add one for every iteration
        tot_1 = tot_1+1
        #if x is less than the percentile
        if x < percentile:
            #add one to counter num_1
            num_1=num_1 +1
        #if x is greater than percentile 
        elif x > percentile:
            #add 1 to num_2
            num_2 = num_2+1
    #let the user know how many seqs are below a specific percentile and how many are above a specific percentile.
    print "%s percentile is: %s seqs below this percentile = %s above percentile = %s" %(p,  np.percentile(array,p), num_1, num_2)
#print total number of sequences.
print tot_1
#plot a boxplot of the data.
plt.boxplot(boxplot_data)
#show the data too. Wait until its closed to continue the script.
plt.show(block=False)
#sort boxplot_data list.
boxplot_data = sorted(boxplot_data)
#tell user to save plot if they want too.
print "Save plot if you don't want it to close before entering percentile."
#ask user what percentile they want to use as a cutoff for collecting seqs for pipeline below
var = raw_input( "What percentile should I cut off at? (Insert a number no percentage sign, between 1-100)")
#tell user what they entered.
print "You entered %s" %(var)
#make empty dictionary called seqs_above_per, is where the seqs above percentile and their gid will go.
seqs_above_per = {}
#check that the number given is within the allowable range of 0-100.
if (int(var) > 0) and (int(var) <= 100):
    #tell user number is within range
    print "number within range, will extract sequences above the %s percentile." %(var)
    #loop though seqs dict.
    for seq in seqs_dict:
        #if seqs dict is greater than or equal to the number corresponding to the percentile picked
        if int(seqs_dict[seq][1]) >= np.percentile(array,int(var)):
            #add the gid as the key and the sequence as the value to the seqs_above_per dict.
            seqs_above_per[seq] = seqs_dict[seq]
#number not within range
else:
    #tell user number not within range.
    print "number not within range"
#open a new file where the fasta seqs above the percentile chosen will be placed
new_seq_file = open("%s_%s_percentile.fasta" %(fasta_in_split[0],var),'w')
#loop through dict seqs_above_per
for seq in seqs_above_per:
    #write the seqs and their gid in fasta format into the file above.
    new_seq_file.write(">%s\n%s\n" %(seq, seqs_above_per[seq][0]))
#when done with loop close file
new_seq_file.close()
#import my custom module phylo_tools    
import phylo_tools
#import my other module called cdt_tools.
import cdt_tools
#input just the main name without the fa extension.
print "%s_%s_percentile" %(fasta_in_split[0],var)
#run unaligned list of fasta seqs through clustal omega and get a aligned fasta seq file.
phylo_tools.ClustalO("%s_%s_percentile" %(fasta_in_split[0],var))
#input aligned fasta seqs into FastTreeMP and get a newick tree output.
phylo_tools.FastTreeMP("%s_%s_percentile_clustalo" %(fasta_in_split[0],var))
#convert the aligned fasta seqs and newick file to cdt format to view in java treeview.
phylo_tools.fasta2cdt("%s_%s_percentile_clustalo" %(fasta_in_split[0],var))
#add taxid to cdt file using blastdbcmd.
cdt_tools.add_taxid("%s_%s_percentile_clustalo.cdt" %(fasta_in_split[0],var))


