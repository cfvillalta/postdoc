#!/usr/bin/env python
#the python script takes two files, SNP data downloaded from 23andme and a list of one snp on each line of all the snps present on SNPedia that I collected using wikitools.
import sys
import re
from wikitools import *

#import  23andme SNP filepath into string.
genome_file = sys.argv[1]
#open 23andme data file
snp_in = open(genome_file,'r')
#read 23andme data into a list snp_data
snp_data = snp_in.readlines()
#import list of snps filepath into string
snpedia_list_file = sys.argv[2]
#open snp list file
snp_in_2 = open(snpedia_list_file, 'r')
#read snps into a list called snpedia_data
snpedia_data = snp_in_2.readlines()
#make a dictionary to read 23andme data into.
snp_23andme = {}
#make a list to read snpedia data into
snp_snpedia = []
#counter set to zero, integer variable
counter = 0
#loop through snpedia_data
for snp in snpedia_data:
    #strip whitespace.
    snp = snp.strip()
    #make all letters lower case because it shows up as Rs and I want it rs to match 23andme format.
    snp = snp.lower()
    #add each snp as a string to snp_snpedia list.
    snp_snpedia.append(snp)
#loop through 23andme data.
for snp in snp_data:
    #if starts with rsid thats the header
    if snp.startswith('rsid'):
        #strip whitespace of header and store as a string called header.
        header=snp.strip()
    #else if the snp starts with 'rs' its a snp id
    elif snp.startswith('rs'):
        #strip of whitespace
        snp=snp.strip()
        #split the string by \t, the first string from the split is the snp
        snp_s = snp.split('\t')
        #add one to counter
        counter = counter+1
        #if the snp is in the snpedia data list then
        if snp_s[0] in snp_snpedia:
            #add the snp id as the key and the snp information as the value to the snp_23andme dictionary.
            snp_23andme[snp_s[0]]= snp_s
#open new file where I will put the snp data I collect from snpedia for snps that are present in both my 23andme data set and snpedia.
snp_dict_text = open('snp_data_out.dict', 'w')
#my second counter set to zero
counter_2 = 0
#loop through snp_23andme dictionary
for snp in snp_23andme:
    #for every new snp counter increased by 1 
    counter_2=counter_2+1
    #use wikitools to access snpedia bot site. Action is called site
    site = wiki.Wiki("http://bots.snpedia.com/api.php")
    #in pangehandle I call up the site and see if the sno is present in there.
    pagehandle = page.Page(site,snp)
    #try the commands below if doesnt work move to except
    try:
        #try to grab page info only works if snp is present.
        snp_page = pagehandle.getWikiText()
        #write SNP id to snp_data_out.dict
        snp_dict_text.write('SNP=%s\n'%(snp))
        #write webpage data to snp_data_out.dict and when it begins and ends.
        snp_dict_text.write('SNPEDIA_DATA_BEGIN\n%s\nSNPEDIA_DATA_END' %snp_page)
    #if try does not work move to except
    except:
        #tells me snp not found
        print 'SNP not found.'
        #move along
        pass
    #print out what snp I am on out of how many snps using the two counters. Counter2 is slowly increasing and counter already has the full number of snps.
    print '%s out of %s\t%s' %(counter_2,counter,snp)
#close the snp_data_out.dict file.
snp_dict_text.close()    
