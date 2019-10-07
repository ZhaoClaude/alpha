import numpy as np
import math
import csv
import sys
import os
import matplotlib.pyplot as plt
import datetime as dt
from WindPy import *


def performance2():
    tdate = startdate
    j = 0
    changedate.append(enddate)
    while tdate<=enddate:


        backdata = getdata(codelist,timelist)
        ret = backdata*alpha

        j = j+1;
        tdate = changedate[j]





def listread(filename):
    return []

def getdata(codelist,datelist,atype):
    
    data = []
    print(datelist)
    for i in codelist:
        temp = w.wsd(i,atype,datelist[0],datelist[1]).Data[0]
        data.append(temp)
    data =np.array(data).T
    print('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv')
    np.savetxt('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv',data,delimiter=',')
    return(data)
        
def getdatacsv(codelist,datelist,atype):
    data = np.loadtxt('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv',delimiter=',')
    return(data)
    
def alphatest(data):
    alphaout = np.ones([data[0].shape[0]-1,data[0].shape[1]])
    return alphaout
    
def computeret(close,pos):
    ret = close[1:]/close[:-1]
    
    pos = (pos.T/np.sum(pos,axis = 1)).T
    pnlret = np.sum(pos*ret,axis = 1)
    
    return list(pnlret)

def performance(ret):
    pnl =[1]
    maxprofit = 0
    maxdrawdown = 0
    ret = np.array(ret)
    for i in ret:
        pnl.append(pnl[-1]*i)

        maxprofit = max(maxprofit,pnl[-1])
        maxdrawdown = max([maxprofit-pnl[-1],maxdrawdown])
    sharpe =np.mean(ret-1)/np.std(ret-1)*(252**0.5)
    #np.savetxt('test.csv',ret)
    print ("the final pnl is ",pnl[-1])
    print ("the maxdrawdown is",maxdrawdown)
    print("the shapre ratio is",sharpe)
    plt.plot(pnl)
    plt.show()
    


def backtestalpha(startdate,enddate,changedate,subuniversepath,alphatype):
    w.start()
    tdate = startdate
    j = 0
    changelist = listread(changedate)
    ret = []
    changelist.append(enddate)
    while (tdate<= enddate) and(j<len(changelist)) :
        data = []
        codelist = w.wset("sectorconstituent","date="+tdate.strftime('%Y%m%d')+";windcode="+subuniversepath+';field= wind_code').Data[0]
        #codelist = ['000016.sh']
        datelist = [tdate,w.tdaysoffset(1, changelist[j], "").Data[0][0].date()]
        for i in alphatype:
            data.append(getdata(codelist,datelist,i))
        alphaout = alphatest(data)
        ret.extend(computeret(data[0],alphaout))
        
        tdate = changelist[j]
        j = j+1
    
    performance(ret)
    
    return 0

        





# config
startdate = dt.date(2019,3,1)  # minimum startdate=20100101
enddate = dt.date(2019,9,1)
changedate = 'change.csv'
backdate = 5  # number of previous days necessary for calculating today's position; e.g., if you need Tue,Wed,Thu data to calculate Fri position, set backdate=3; minimum backdate is 1
booksize = 1e7  # the total portfolio monetary size (RMB)
mode = 0  # 0 for long only without hedging; 1 for long only with futures hedging; 2 for long-short
universe = 0  # 0 for all A share; 1 for subuniverse: set subuniversepath
subuniversepath = '000300.SH'  # ZZ800 for 'zhongzheng800', HS300 for 'hushen300'
pnlpath = 'pnl.csv'  # output pnl file
positionpath = 'position.csv'  # output daily position file
tradingcost = 8e-4
futurestradingcost = 0.6e-4
alphatype = ['close']
backtestalpha(startdate,enddate,changedate,subuniversepath,alphatype)
#performance()

