#!/usr/bin/env python 

import sys
import re
from wikitools import *
#import data from 23andme SNP file.
genome_file = sys.argv[1]
snp_in = open(genome_file,'r')
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
        
keyword =re.compile('pathogenic',re.IGNORECASE) 


snps_no_snpedia = []
snp_dict_text = open('snp_data_out.dict', 'w')
for snp in snp_dict:

    site = wiki.Wiki("http://bots.snpedia.com/api.php")
#print snp
#print site
    
    pagehandle = page.Page(site,snp)
    try:
        snp_page = pagehandle.getWikiText()
        if keyword.search(snp_page):
            snp_dict_text.write('SNP=%s\n'%(snp))
            snp_dict_text.write('SNPEDIA_DATA=\n%s' %snp_page)
            print 'SNPedia data available for %s\tputatively pathogenic' %(snp)
        else:
            print 'SNPedia data available for %s\t no pathogenic data' %(snp)
    except:
        snps_no_snpedia.append(snp)
        print 'no SNPedia data present for %s' %(snp)
        
snp_dict_text.close()
print 'all done'

snp_no_data = open('list_snps_no_snpedia_data.list','w')
for snp in snps_no_snpedia:
    snp_no_data.write("%s\n" %(snp))
    
#print snps_no_snpedia
snp_no_data.close()
        

