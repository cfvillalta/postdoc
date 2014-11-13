#!/usr/bin/env python

import sys
import re
from wikitools import *

snp_file = sys.argv[1]
snp_in = open(snp_file, 'r')
snp_data = snp_in.readlines()

for snp in snp_data:
    snp = snp.strip()
    print snp
