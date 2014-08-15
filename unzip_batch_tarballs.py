#! /usr/bin/python/

from subprocess import Popen
import os
import sys

program = 'tar'

folder_tars = sys.argv[1]
print folder_tars

files = os.listdir (folder_tars)

for file in files:
    if file.endswith(".tar.gz"):
        p = Popen([program,'-zxvf', '%s%s' %(folder_tars,file), '-C', '%s' %(folder_tars)])
        p.communicate('file done being uncompressed')
        
