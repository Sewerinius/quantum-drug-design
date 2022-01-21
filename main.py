#!/bin/python

import os
from io import StringIO

import pandas as pd

PDB_FILE = "inputs/test.pdb"
ONEBODY_BEGIN_TAG = '[BEGIN ONEBODY SEQPOS/ROTINDEX/ENERGY]'
ONEBODY_END_TAG = '[END ONEBODY SEQPOS/ROTINDEX/ENERGY]'
TWOBODY_BEGIN_TAG = '[BEGIN TWOBODY SEQPOS1/ROTINDEX1/SEQPOS2/ROTINDEX2/ENERGY]'
TWOBODY_END_TAG = '[END TWOBODY SEQPOS1/ROTINDEX1/SEQPOS2/ROTINDEX2/ENERGY]'

os.system(f"rscript/rosetta_scripts -parser:protocol script.xml -scorefile_format json -s {PDB_FILE}")

with open('out.txt', 'r') as f:
    file_text = f.read()

onebody_begin = file_text.find(ONEBODY_BEGIN_TAG) + len(ONEBODY_BEGIN_TAG) + 1
onebody_end = file_text.find(ONEBODY_END_TAG, onebody_begin)
twobody_begin = file_text.find(TWOBODY_BEGIN_TAG, onebody_end) + len(TWOBODY_BEGIN_TAG) + 1
twobody_end = len(file_text) - len(TWOBODY_END_TAG) - 2

onebody_text = file_text[onebody_begin:onebody_end]
twobody_text = file_text[twobody_begin:twobody_end]

onebody_energies = pd.read_csv(StringIO(onebody_text), sep='\t', names=['position', 'rotameter_index', 'energy'])
twobody_energies = pd.read_csv(StringIO(twobody_text), sep='\t', names=['position_1', 'rotameter_index_1', 'position_2', 'rotameter_index_2', 'energy'])

print(onebody_energies)