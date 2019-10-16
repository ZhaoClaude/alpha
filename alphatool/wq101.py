# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:10:40 2019

@author: lenovo
"""

import numpy as np
import scipy.stats as ss

def rankdata(x):
    t = (ss.rankdata(x)-1)/(x.shape[-1]-1)
    return(t)

def delta(data,backday,nsize):
    return data[nsize::]-data[nsize-backday:0-backday]

def tsmax(x,backday,nsize):
    t  = []
    for i in range(nsize,len(x)):

        t.append(np.max(x[i-backday:i+1],axis = 0))
        
            
    return(np.array(t))

def tsmin(x,backday,nsize):
    t  = []
    for i in range(backday,len(x)):

        t.append(np.min(x[i-backday:i+1],axis = 0))
        
            
    return(np.array(t))
    
#    
#if __name__== '__main__':
#    t1 = wq101()
    
