#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Sai Venkatesh Kurella
"""

import csv
import math
import matplotlib.pyplot as plt
import sys
import time
import glob
from bs4 import BeautifulSoup
import codecs
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from collections import Counter 
import re 
import numpy as np


path = str(sys.argv[1]+'/files/*.html')


def load_data(path,data,size):   
    files=glob.glob(path) 
    files = files[:size]
    for file in files: 
        f=codecs.open(file, 'r',encoding='utf-8', errors='ignore')  
        data.append(BeautifulSoup(f.read(), 'html.parser').get_text())
        f.close()
    return files


def sort_by_length(data):
    len_data = [len(x) for x in data]
    zipped = list(zip(len_data,data))
    out =[y for x,y in sorted(zipped)]
    return out,len_data

def ntf(tokens):
    frq_tok = Counter(tokens)
    norml2= math.sqrt(sum([y for x,y in frq_tok.items()]))
    for x,y in frq_tok.items():
        frq_tok[x]= y/norml2
    return frq_tok

def IDF(data_list):
    full_data =[]
    total_docs= len(data_list)
    for x in data_list:
        full_data.extend(x)
    idf = Counter(full_data)
    for x,y in idf.items():
        idf[x] = math.log10(total_docs/y)
    return idf

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

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
        for x in list(idf.keys()):
            tfidf[x] = 0
        for x,y in tf[i].items():
            try:
                tfidf[x]=idf[x]*y
            except:
                continue
        docu[file.split("/")[-1].split(".")[0]] = tfidf
        
    return tf,idf,docu 
    

tf=[]
idf = Counter()
docu = Counter()
tf,idf,docu =tfidf(path,504)
X =[]
for k,v in docu.items():
    X.append(list(v.values())) # this is tfidf matrix
    
    

   
Z = linkage(X, method='average', metric='cosine')
    

plt.figure(figsize=(100,50))
fancy_dendrogram(Z,show_contracted=True,max_d=0.4)
"""print(X[:100])"""
"""np.set_printoptions(threshold=np.inf)"""
"""np.printoptions(threshold=np.inf)"""
mat = np.matrix(X[:100])
#print(mat)
#print(mat.shape)
for i in mat:
    for j in i[0]:
        print(j, end =" ")
    print()
#for row in mat:
   # for r in row:
 #       print(r),
 #   print()        
plt.savefig('agglomerativedendogram.png')
plt.xticks(fontsize=10)
plt.show()



