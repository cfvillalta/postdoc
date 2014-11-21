#!/usr/bin/env python
#script will input csv file and then make dotplot of data. 
#the script also runs a 2way anova on microconidia data for TYR4 and the vector control using R.
#the script also runs a mann whitney test for every combination of data between TYR4 and vector control. Use scipy

import sys
import re
#get file path to input file which should be a .csv file with conidia numbers. I am counting the number of conidia isolated from plates.
conidia_data = sys.argv[1]
#split file path before file extension type
file_name_split = conidia_data.split(".")
#open conidia data file.
fh = open(conidia_data)
#read lines of conidia data file into list csv.
csv = fh.readlines()
#make a blank dictionary called data
data = {}
#make a blank list called header.
header = []
#loop through csv list
for line in csv:
    #sample is a re pattern that looks for lines with a pCV id which will have the conidia data
    sample = re.compile(r"(pCV\d+\-\d)")
    #search line for sample pattern and not if there is a match.
    match = sample.search(line)
    #if there is a match
    if match:
        #strip line of whitespace
        line = line.strip()
        #split data in line by comma ,
        lines = line.split(",")
        #move string from lines[0] into data_name thats the data id....pCV...
        data_name = lines[0]
        #input data_name as a key in data dictionary and use the lines list as the value.
        data[data_name] = lines
    #if no match its the header
    else:
        #remove whitespace on front and end.
        line = line.strip()
        #split lines by comma
        lines = line.split(",")
        #copy lines list to header.
        header = lines


#going to organize data by tyr.
#make empty dictionary called tyrs.
tyrs = {}
#loop through data dictionary
for sample in data:
    #if tyr type present in tyrs
    if data[sample][2] in tyrs:
        #if light or dark present already
        if data[sample][3] in tyrs[data[sample][2]]:
            #add new data to list that is already present for type of tyr light or dark. 
            tyrs[data[sample][2]][data[sample][3]].append(data[sample])
        else:
            #add new light or dark as key to dictionary value in  the tyrs dict and input data into list for dict within dict.
            tyrs[data[sample][2]][data[sample][3]]=[data[sample]]
    #if tyr key not present yet in list 
    else:
       # create new dictiorary entry with tyr type as key. with an emptyy dictionary as a value (will include light or dark ask key and a list as the value that will inclue data from the sample in the loop).
        tyrs[data[sample][2]]={}
        #add in light or dark as value to dictionary/key to subdictionary. Add sample data which is value from data dictionary as the value to the dict in the dict.
        tyrs[data[sample][2]][data[sample][3]]=[data[sample]]
#tyrs e.g. vector_light, vector_dark,tyr_light, tyr_dark
#create an empty dictionary called data_to_plot.
data_to_plot = {}
#counter to count the number of conditions.
num_cond = 0
#loop through tyrs dict
for tyr in tyrs:
    #loop through dictionary within tyrs dict
    for cond in tyrs[tyr]:
        #add one to number of conditions
        num_cond = num_cond+1
        #make a key that is the typpe of tyr and cond joined by an underscore as the key to new dictionary that will have data to plot. Value is empty list I will append to later
        data_to_plot["%s_%s" %(tyr, cond)]= []
#make a list called conditions list with an empty string in it. Will appened more later, have an empty string in there for graph formatting purposes.
condition_list = ['']
#loop though dict of tyrs, but sorted
for tyr in sorted(tyrs):
    #loop through subdictionary.
    for cond in tyrs[tyr]:
        #add to the list the type of microcondia conditions e.g. tyr1_light_microconidia
        condition_list.append('%s_%s_microconidia' %(tyr,cond))
        #add to the list the type of macrocondia conditions e.g. tyr1_light_macroconidia
        condition_list.append('%s_%s_macroconidia' %(tyr,cond))

import numpy as np
#make blank list called dotplot data
dotplot_data=[]
#sort dict and then loop through it.
for name in sorted(data_to_plot.keys()):
    #split by underscore
    name_split = name.split("_")
    #match criteria to match tyrs, using strings made from split above.
    tyr_match = re.compile(name_split[0])
    #match criteria to match condition using strings made from split above.
    cond_match = re.compile(name_split[1])
    #blank list called add_list
    add_list = []
#MICROCONIDIA
    #loop thorugh tyrs dict.
    for tyr in tyrs:
        #loop through dict within dict.
        for cond in tyrs[tyr]:
            #loop through list in dict of dictionary
            for sample in tyrs[tyr][cond]:
                #see if tyr_match matches the tyr.
                match = tyr_match.search(tyr)
                #see if cond_match matches the cond
                match_2 = cond_match.search(cond)
                #if match and match_2 have matches present from re.search
                if match and match_2:
                    #microconidia
                    #extract microconidia data from sample list. Convert to a floating point number and log10 transform it.
                    log10_sample = np.log10(float(sample[4]))
                    #if the number is equal to zero, add a zero to the list.
                    if float(sample[4]) == 0:
                        add_list.append(0)
                    #if the number is not zero add the log10_sample floating point number to add_list list.
                    else:
                        add_list.append(log10_sample)
    #appenend list to list called dotplot_data. Now a list of lists.
    dotplot_data.append(add_list)
    #overwrite add_list with an empty list.
    add_list=[]                    

#MACROCONIDIA 
#Do the same thing I did with the microconidia except I am grabbing data for macroconidia.
    for tyr in tyrs:
        for cond in tyrs[tyr]:
            for sample in tyrs[tyr][cond]:
                match = tyr_match.search(tyr)
                match_2 = cond_match.search(cond)
                if match and match_2:
                    log10_sample =  np.log10(float(sample[5]))
                    if float(sample[5])==0:
                    #macroconidia      
                        add_list.append(0)
                    else:
                        add_list.append(log10_sample)
    dotplot_data.append(add_list)

####################
#2 way annova
#looking at 2 conditions wheter light and dark make a difference or if genotype makes a difference.
####################
from numpy import *
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
#genotype vector or tyr4
#ld  is light or dark
#only for microconidia
#empty dictionary called genotype
genotype = {}
#counter at zero to count number of genotypes.
num_genotypes = 0
#counter to count number of samples
num_samples  = 0
#list to list the number of conditions.
conditions = []
#loop through tyr again.
for tyr in sorted(tyrs):
    #count number of genotypes
    num_genotypes = num_genotypes +1
    #loop through conditions for each tyr (dict in dict)
    for cond in sorted(tyrs[tyr]):
        #light or dark loop
        #if the condition is in our new list called coniditions pass
        if cond in conditions:
            pass
        #if conidition is not
        else:
            #add condition to the list conditions
            conditions.append('"%s"' %(cond))
        #loop through each sample for the tyr and cond
        for sample in tyrs[tyr][cond]:
            # use counter to count the number of samples
            num_samples = num_samples+1
            #if the tyr in the genotype dictionary add log fold transformed microconidia count data to list of other counts.
            if tyr in genotype:
                genotype[tyr].append(str(np.log10(float(sample[4]))))
            #if the tyr is not present add a new key to dictionary and the appropriate microconidia count data.
            else:
                genotype[tyr]=[str(np.log10(float(sample[4])))]
#wanted to calculate the number of samples for each genotype
num_each_genotypes  = num_samples/num_genotypes
#counting the number of coniditions present
num_conditions = len(conditions) 
#blank genotype list
genotype_list = []
#blank second genotype list
genotype_list2 = []
#loop through genotype dictionary
for g in genotype:
    #running r in python naming a list that I will input microconidia data into.
    ro.r('%s_list = c(%s)' %(g,','.join(genotype[g])))
    #making a list of genotypes in python
    genotype_list.append('"%s"'%(g))
    #second list of genorypes with the _list joined to the genotype.
    genotype_list2.append('%s_list'%(g))
#make a array in python called knockdown genotypes that will contain the types of genotypes present. e.g. tyr4_list
ro.r('kd_genotype=c(%s)' %(','.join(genotype_list2)))
#make a general linear group matrix, with the number of conditions and the number of samples. label with the types of conditions.(light or dark)
ro.r('conditions =gl(%s,1,%s,labels=c(%s))' %(num_conditions,num_samples,",".join(conditions)))
#make another general linear group matrix with the number of genotypes, the number of each genortype and the number of total samples. populate with the types of genotype e.g. (vector and TYR4)
ro.r('geno=gl(%s,%s,%s,labels=c(%s))' %(num_genotypes,num_each_genotypes,num_samples,",".join(genotype_list)))
#run the 2 way annova in R. Output will be printed to the screen.
print ro.r('anova(lm(kd_genotype~conditions*geno))')

#now need to work on t-test or signle test stat to see if its sign. Multiple hypothesis testing too.
#can do mannwhitney test using scipy
from scipy.stats import mannwhitneyu
#make a blank list to place cond_pairs into
cond_pairs = []
#make a blank dictionaru to put condition pairs into for mann whitney test
cond_pairs_mwt ={}
#loop through condition list
for cond_a in condition_list:
    #loop through condition list again
    for cond_b in condition_list:
        #if the two conditions are the same pass.
        if cond_a is cond_b:
            pass
        #if one of the conditions is an empty string pass
        elif cond_a is '' or cond_b is '':
            pass
        #else if non of the above, the conditions must be different. 
        else:
            #place cond_a and cond_b into a list called cond_list
            cond_list = [cond_a, cond_b]
            #sort cond_list
            cond_list = sorted(cond_list)
            #if the list is present in the list of lists called cond_pairs pass.
            if cond_list in cond_pairs:
                pass
            #if its not 
            else:
                #add cond_list to cond_pairs list (now a list of lists)
                cond_pairs.append(cond_list)
                #split condition into list at the underscore for cond_a and cond_b
                cond_a_split = cond_a.split("_")
                cond_b_split = cond_b.split("_")
                #if the two strings from the list above match
                if cond_a_split[2] ==  cond_b_split[2]:
                    #if they are the string microconidia
                    if cond_a_split[2] == 'microconidia':
                        #create two empty lists for two sets of bioreps a and b
                        bioreps_a = []
                        bioreps_b = []
                        #loop through microcondiia data for the specific genotype and condition above by going through the tyrs dict and the subdictiony within with conditions.
                        for x in tyrs[cond_a_split[0]][cond_a_split[1]]:
                            #convert the string to floating point numbers
                            bioreps_a.append(float(x[4]))
                        #do the same as above for condition b
                        for x in tyrs[cond_b_split[0]][cond_b_split[1]]:
                            bioreps_b.append(float(x[4]))
                        #run mann whitney test using scipy
                        mw_test =  mannwhitneyu(bioreps_a,bioreps_b)
                        #in condition pairs mwt use the cond_list string with the type of conditions being compared as the key and the mw_test output as the value. 
                        cond_pairs_mwt["%s" %("\t".join(cond_list))] = mw_test
#STOPPED HERE
pval_sort = []
for x in sorted(cond_pairs_mwt):
    pval_sort.append(str(cond_pairs_mwt[x][1]))
#    print cond_pairs_mwt[x][1]

ro.r('pval = c(%s)' %(",".join(pval_sort)))
#print ro.r('pval')
#print ro.r('length(pval)')
padjust = ro.r('p.adjust(pval, method="BH",n=length(pval))')
#print padjust
n=0

#header
print "Conditions\tp_value\tadjusted_p_value"
for x in sorted(cond_pairs_mwt):
    print "%s\t%s\t%s" %(x,cond_pairs_mwt[x][1],padjust[n])
    print
    n=n+1

##############
#organzing data for graphing
##############

import random
num = 0
y_axis_points = []
x_axis_points= []
for x in dotplot_data:
    num = num+1
#    print num
    bioreps = len(x)
    a=num-.15
    b=num+.15
    x_axis = [random.uniform(a,b) for p in range(0, bioreps)]
    x_axis_points.extend(x_axis)
    y_axis_points.extend(x)



import wx
import matplotlib as mpl
mpl.use('WXAgg')
import pylab

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax=plt.gca()
ax.set_xticklabels(condition_list, rotation =90)
plt.axis(ymin=0,ymax=10,xmin=0,xmax=num+1)
plt.plot(x_axis_points, y_axis_points, 'ro')
fig.tight_layout()
plt.show()
