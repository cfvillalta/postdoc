#!/usr/bin/env python

import sys
import re
from wikitools import *

snp_file = sys.argv[1]
snp_file_s = snp_file.split(".")
snp_in = open(snp_file, 'r')
snp_data = snp_in.readlines()
snp_dict_text = open('%s_data_out.txt' %(snp_file_s[0]), 'w')
keyword =re.compile('pathogenic',re.IGNORECASE) 
for snp in snp_data:
    snp = snp.strip()
    #print snp
    site = wiki.Wiki("http://bots.snpedia.com/api.php")
    pagehandle = page.Page(site,snp)
    try:
        snp_page = pagehandle.getWikiText()
        if keyword.search(snp_page):
            snp_dict_text.write('SNP=%s\n'%(snp))
            snp_dict_text.write('SNPEDIA_DATA=\n%s' %snp_page)
            print 'SNPedia data available for %s\tputatively pathogenic %s' %(snp,snp_file)
        else:
            print 'SNPedia data available for %s\t no pathogenic data %s' %(snp,snp_file)
#            pass
    except:
        pass
        print 'no SNPedia data present for %s %s' %(snp, snp_file)
        
snp_dict_text.close()

status_file = open('done_extracting_snpedia_data.txt', 'w')
status_file.write('%s_data_out.txt' %(snp_file_s[0]))
status_file.close()


    
#print snps_no_snpedia

