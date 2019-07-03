#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Author: Sai Venkatesh Kurella
"""
"""Importing the required Libraries"""
import sys
import csv
import math
import time
import glob
import matplotlib.pyplot as plt
import codecs
from bs4 import BeautifulSoup
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
    data_len = [len(x) for x in data]
    zipped = list(zip(data_len,data))
    out =[y for x,y in sorted(zipped)]
    return out,data_len
"""Finding the term frequency"""
def ntfreq(tokens):
    tok_freq = Counter(tokens)
    norml2= math.sqrt(sum([y for x,y in tok_freq.items()]))
    for x,y in tok_freq.items():
        tok_freq[x]= y/norml2
    return tok_freq
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
    files =load_data(path, data, size)
    
    data,len_dat = sort_by_length(data)
    len_dat.sort()
    tf =[{}]*len(data)
    for i,file in enumerate(files):
        token=list(filter(None,re.findall('[a-zA-Z]+|[.,!?;]+|\\d+',data[i].lower())))
        tokens.append(token)
        tf[i]= ntfreq(token)
        
    idf = IDF(tokens)
            
    for i,file in enumerate(files):
        tfidf={}
        for x,y in tf[i].items():
            try:
                tfidf[x]=idf[x]*y
            except:
                continue
        with open(sys.argv[2]+'\\'+file.split("/")[-1].split(".")[0]+'.wts', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for keys,values in tfidf.items():
                writer.writerow([keys,values])
           
for j in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
    start = time.time()
    tfidf(path,j)
    end = time.time()
    timer.append(end-start)

"""Plotting the Graph"""
plt.scatter([10, 20, 40, 80, 100, 200, 300, 400, 500],timer)
plt.title('Computation Cost of TFIDF with # Documents')
plt.xlabel('# Documents')
plt.ylabel('Time in seconds')
plt.savefig(sys.argv[2]+'tfidf_time.png')
plt.show()

