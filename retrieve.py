  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sai Venkatesh Kurella
"""

import glob
import os 
from collections import Counter
import re
import sys

cw_path = os.getcwd()
src = cw_path+'/Outputs/*.wts'
doc = {}
files = glob.glob(src)
for file in files:
    d = {}
    fname = file.split("/")[-1].split(".")[0]
    with open(file) as f:
        for line in f:
            if len(line.split(',')) >2: 
                continue
            else:
                (key, val) = line.split(',')
                d[key] = float(val)
    doc[fname]= d


query= sys.argv[1]

process=list(filter(None,re.findall('[a-zA-Z]+|[.,!?;]+|\\d+',query.lower())))
weight = [float(s) for s in sys.argv[2].split(' ')]
 
out = Counter()

for fn, vocab in doc.items():
    w = 0 
    for i,tok in enumerate(process):
        if tok in vocab.keys() :
            w += vocab[tok] * weight[i]
    out[fn]=w

for ky,val in out.most_common(10) :
    print(ky+".html"+" "+str(val))
