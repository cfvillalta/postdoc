#! /usr/bin/python/
#program opens multiple tar.gz files in the same directory. Made the script to open ncbi nr database tar files to build nr locally.
from subprocess import Popen
import os
import sys
#name the program I am going to use
program = 'tar'
#get file path of folder where all the tar files are.
folder_tars = sys.argv[1]
#print the folder name so I cam make sure I di it correctly
print folder_tars
#make a list of files in the directory
files = os.listdir (folder_tars)
#loop through the list of files
for file in files:
    #if the file ends in .tar.gz
    if file.endswith(".tar.gz"):
        #run subprocess below on file and uncompress into the same folder.
        p = Popen([program,'-zxvf', '%s%s' %(folder_tars,file), '-C', '%s' %(folder_tars)])
        #wait until file is done compressing and send user message to let them know its done compressing.
        p.communicate('file done being uncompressed')
        
