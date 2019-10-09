# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:10:40 2019

@author: lenovo
"""

from numpy import *


class wq101(object):
    def rankdata(self,x):
        t = (argsort(argsort(x))+1)/(len(x))
        return(t)
        
    
    
    
    def delta(self,data,backday):
        return data[:-backday]
    
if __name__== '__main__':
    t1 = wq101()
    
