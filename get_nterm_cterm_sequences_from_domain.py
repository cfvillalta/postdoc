#in this script I want to input a file with specific domain sequences, e.g. a tyrosinase and extract the n-term and c-term seqs.
#also want to be able to handle sequences with and without multiple domains, e.g. sequences that have multiple tyrosinase sequences.

import sys
import re
import os
from Bio import Phylo
from subprocess import Popen, PIPE
