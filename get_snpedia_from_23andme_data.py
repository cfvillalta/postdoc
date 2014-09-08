#!/usr/bin/env python 

import sys
from wikitools import *
#import data from 23andme SNP file.

snp_in = open('/Users/cfvillalta/genome.txt','r')
snp_data = snp_in.readlines()

snp_dict = {}

for snp in snp_data:
    if snp.startswith('rsid'):
        header=snp.strip()
    elif snp.startswith('rs'):
        snp=snp.strip()
        snp_s = snp.split('\t')
        snp_dict[snp_s[0]]=snp_s
        
#print snp_dict
        
        
        

snps_no_snpedia = []
snp_interest = {}
for snp in snp_dict:

    site = wiki.Wiki("http://bots.snpedia.com/api.php")
#print snp
#print site

    
    pagehandle = page.Page(site,snp)
    try:
        snp_page = pagehandle.getWikiText()
        snp_interest[snp] = snp_page
    except:
        snps_no_snpedia.append(snp)
        
    
#print snps_no_snpedia

        
snp_dict_text = open('snp_data_out.dict', 'w')
snp_dict_text.write(snp_dict)
