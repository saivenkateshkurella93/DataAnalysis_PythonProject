#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Author: Sai Venkatesh Kurella
"""
"""Importing the required Libraries"""
import csv
import math
import matplotlib.pyplot as plt
import sys
import time
import glob
from bs4 import BeautifulSoup
import codecs
from collections import Counter 
import re 
path = str(sys.argv[1]+'*.html')
timer=[]

"""Loading the data from the files"""
def load_data(path,data,size):   
    files=glob.glob(path) 
    files = files[:size]
    for file in files: 
        f=codecs.open(file, 'r',encoding='utf-8', errors='ignore')  
        data.append(BeautifulSoup(f.read(), 'html.parser').get_text())
        f.close()
    return files

"""Sorting the data by length"""
def sort_by_length(data):
    len_data = [len(x) for x in data]
    zipped = list(zip(len_data,data))
    out =[y for x,y in sorted(zipped)]
    return out,len_data
"""Finding the term frequency"""
def ntf(tokens):
    frq_tok = Counter(tokens)
    norml2= math.sqrt(sum([y for x,y in frq_tok.items()]))
    for x,y in frq_tok.items():
        frq_tok[x]= y/norml2
    return frq_tok
"""Finding the Inverse Document frequency"""
def IDF(data_list):
    full_data =[]
    total_docs= len(data_list)
    for x in data_list:
        full_data.extend(x)
    idf = Counter(full_data)
    for x,y in idf.items():
        idf[x] = math.log10(total_docs/y)
    return idf
"""Finding TFIDF"""
def tfidf(path,size):
    data =[]
    tokens=[]
    docu = {}
    files =load_data(path, data, size)
    data,len_dat = sort_by_length(data)
    len_dat.sort()
    tf =[{}]*len(data)
    for i,file in enumerate(files):
        token=list(filter(None,re.findall('[a-zA-Z]+|[.,!?;]+|\\d+',data[i].lower())))
        tokens.append(token)
        tf[i]= ntf(token)
        
    idf = IDF(tokens)
            
    for i,file in enumerate(files):
        tfidf={}
        for x,y in tf[i].items():
            try:
                tfidf[x]=idf[x]*y
            except:
                continue
        docu[file.split("/")[-1].split(".")[0]] = tfidf
        
    return tf,idf,docu 
"""Computing dictionary and posting file"""   
for j in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
    start = time.time()
    tf=[]
    idf = Counter()
    docu = Counter()
    tf,idf,docu =tfidf(path,j)
    dictionary= []
    posting_list=[]
    pos=0
    for x,y in idf.items():
        cnt = 0
        for term in tf:
            if x in term.keys():
                cnt = cnt +1
        dictionary.append((x,cnt,pos))
        pos = pos + cnt
        for fn,ntfidf in docu.items():
            if x in ntfidf.keys():
                posting_list.append((fn,ntfidf[x]))
    end = time.time()
    timer.append(end-start)

with open(sys.argv[2]+'dictionary', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x,y,z in dictionary:
        writer.writerow([x,y,z])
with open(sys.argv[2]+'posting', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x,y in posting_list:
        writer.writerow([x,y])
"""Plotting the Graph"""
plt.scatter([10, 20, 40, 80, 100, 200, 300, 400, 500],timer)
plt.title('Computation Cost Index with # Documents')
plt.xlabel('# Documents')
plt.ylabel('Time in seconds')
plt.savefig(sys.argv[2]+'index_time.png')
plt.show()

