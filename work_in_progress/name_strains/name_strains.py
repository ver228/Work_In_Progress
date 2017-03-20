#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:14:35 2017

@author: ajaver
"""
from difflib import SequenceMatcher
import numpy as np
#import math


def get_close(s1, rest_s, ftype):
    if ftype == 'desc':
        s_min_ratio = -np.inf
        fun = lambda x,y : x>=y
    elif ftype == 'asc':
        s_min_ratio = np.inf
        fun = lambda x,y : x<=y
    
    s_min = ''
    for ss in rest_s:
        s_ratio = SequenceMatcher(None, s1, ss).ratio()
        if fun(s_ratio, s_min_ratio):
            s_min = ss
            s_min_ratio = s_ratio
    
    return s_min


def sort_by_similarity(data, ftype='desc'):
    
    
    
    #greedily find similar strains
    sorted_s = []
    
    s1, rest_s = data[0], data[1:]
    sorted_s.append(s1)
    
    while len(rest_s) > 1:
        s_min = get_close(s1, rest_s, ftype)
        sorted_s.append(s_min)
        
        rest_s.remove(s_min)
        s1 = s_min
        
    sorted_s += rest_s
    
    return sorted_s

if __name__ == '__main__':
    fname = 'CeNDR_strains.txt'
    with open(fname, 'r') as fid:
        strains = fid.read().split('\n')
    sorted_s = sort_by_similarity(strains)


#%%
numbers = [format(x, '#04x')[2:].upper() for x in range(256)]
numbers = sort_by_similarity(numbers, ftype='asc')

rows = [y + ' ' + x for x, y in list(zip(numbers, sorted_s))]

