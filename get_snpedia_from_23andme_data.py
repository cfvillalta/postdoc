#!/usr/bin/env python 

import sys
import re
from wikitools import *
#import data from 23andme SNP file.
genome_file = sys.argv[1]
snp_in = open(genome_file,'r')
snp_data = snp_in.readlines()

snp_dict = {}
snp_groups = {}
total_snp = 0
counter = 0
group_num = 0
for snp in snp_data:
    if snp.startswith('rsid'):
        header=snp.strip()
    elif snp.startswith('rs'):
        snp=snp.strip()
        snp_s = snp.split('\t')
        if group_num in snp_groups:
            snp_groups[group_num].append(snp_s[0])
        
        else:
            snp_groups[group_num]=[snp_s[0]]
        snp_dict[snp_s[0]]= snp_s
        total_snp = total_snp+1
        if counter <1000:
            counter = counter +1
        else:
            counter = 0
            group_num = group_num+1
#print snp_dict
#print total_snp
#print snp_groups
#for x in snp_groups:
 #   print x

#will split up groups of 1000 into files.With the name snp_group_"num" eg. snp_group_0
from subprocess import Popen, PIPE
import os

input_dir = os.path.dirname(genome_file)

make_dir = Popen(['mkdir', '%s/snp_groups' %(input_dir)])
make_dir.communicate()
print input_dir

list_file_paths = []

counter = 0
for group in snp_groups:
    rel_path = "snp_groups/snp_group_%s.txt" %(group)
    abs_file_path = os.path.join(input_dir, rel_path)
    list_file_paths.append(abs_file_path)
    snp_group_file = open(abs_file_path, 'w')
    snp_group_file.write("\n".join(snp_groups[group]))
    snp_group_file.close()
    counter = counter+1
    if counter > 25:
        print abs_file_path
        run_snp_script = Popen(['python', 'input_snp_list_print_data_out.py', '%s' %(abs_file_path)])
        run_snp_script.communicate()
        counter = 0
        
        
    else:
  #      counter = counter+1
  #      print counter
        print abs_file_path
        run_snp_script = Popen(['python', 'input_snp_list_print_data_out.py', '%s' %(abs_file_path)]) 
        

#run_snp_script = Popen(['python', 'input_snp_list_print_data_out.py', '/Users/cfvillalta/Downloads/snp_groups/snp_group_0.txt'])


'''        
keyword =re.compile('pathogenic',re.IGNORECASE) 


snps_no_snpedia = []
snp_dict_text = open('snp_data_out.dict', 'w')
for group in snp_groups:
    for snp in snp_groups[group]:
        

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
        
'''
