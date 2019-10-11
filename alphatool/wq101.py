# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:10:40 2019

@author: lenovo
"""

from numpy import *


def rankdata(x):
    t = (argsort(argsort(x))+1)/(len(x))
    return(t)

def delta(data,backday,nsize):
    return data[nsize-backday:0-backday]-data[nsize::]

#    
#if __name__== '__main__':
#    t1 = wq101()
    
