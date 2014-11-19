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

snp_23andme = {}
snp_snpedia = []

for snp in snpedia_data:
    snp = snp.strip()
    snp = snp.lower()
    snp_snpedia.append(snp)

#print snp_snpedia
counter = 0
for snp in snp_data:
    if snp.startswith('rsid'):
        header=snp.strip()
    elif snp.startswith('rs'):
         snp=snp.strip()
         snp_s = snp.split('\t')
         if snp_s[0] in snp_snpedia:
             snp_23andme[snp_s[0]]= snp_s
             counter = counter+1
             print counter
#print snp_23andme
#print counter

snp_dict_text = open('snp_data_out.dict', 'w')
counter_2 = 0
for snp in snp_23andme:
    counter_2=counter_2+1    

    site = wiki.Wiki("http://bots.snpedia.com/api.php")
#print snp
#print site
    
    pagehandle = page.Page(site,snp)
    try:
        snp_page = pagehandle.getWikiText()
 
        snp_dict_text.write('SNP=%s\n'%(snp))
        snp_dict_text.write('SNPEDIA_DATA_BEGIN\n%s\nSNPEDIA_DATA_END' %snp_page)
    except:
        print 'SNP not found.'
        pass
    print '%s out of %s\t%s' %(counter_2,counter,snp)
snp_dict_text.close()    
