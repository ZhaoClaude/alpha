import numpy as np
import math
import csv
import sys
import os
import matplotlib.pyplot as plt
import datetime as dt
from WindPy import *
from alphatool import wq101 as wq

    

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
    for i in codelist:
        temp = w.wsd(i,atype,datelist[0],datelist[1],"PriceAdj=F").Data[0]
        data.append(temp)
    data =np.array(data).T
    print('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv')
    np.savetxt('histdata\\'+'000016'+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv',data,delimiter=',')
    return(data)
        
def getdatacsv(codelist,datelist,atype):
    print('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv')
    data = np.loadtxt('histdata\\'+'000016'+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv',delimiter=',')
    return(data)




    

def alphatest(data,backday):
    return alphatest12(data,backday);

def alphatest12(data,backday):
    close = data[0][:-1]
    volume = data[1][:-1]
    
    alpha = np.zeros([data[0].shape[0]-backday-1,data[0].shape[1]])
    alpha = np.sign(wq.delta(volume,backday,backday))*(-1*wq.delta(close,1,backday))
    alpha[alpha<=0] = 0
    return(alpha)
    
 #   for i in range(backday,len(close)-1):


#def alphatest51(data,backday):
#    close = data[0]
#    alphaout = np.zeros([data[0].shape[0]-backday-1,data[0].shape[1]])
#    for i in range(backday,len(close)-1):
#        t1 = (close[i-backday]-close[i-10])/10
#        t2 = (close[i-10]-close[i-1])/10
#        alphaout[i-backday][(t1-t2)<-0.05]=1
#        alphaout[i-backday][(t1-t2)>=-0.05] = -1*(close[i-1][(t1-t2)>=-0.05]-close[i-1][(t1-t2)>=-0.05])
#        alphaout[i-backday][alphaout[i-backday]<0]=0
#        
#    return alphaout
    
        
def alphatest11(data,backday):
    close = data[0]
    vwap = data[1]
    volume = data[2]
    alphaout = np.zeros([data[0].shape[0]-backday-1,data[0].shape[1]])
    for i in range(backday,len(close)-1):
        temp = vwap[i-backday:i]-close[i-backday:i]
        t2 = np.max(temp,axis = 0)
        t3 = np.min(temp,axis = 0)
        t4 = volume[i-1]-volume[i-backday]
        alphaout[i-backday] = (wq.rankdata(t2)+wq.rankdata(t3))*wq.rankdata(t4)
        
        
    print(alphaout.shape)

    #alphaout = np.ones([data[0].shape[0]-backday-1,data[0].shape[1]])
    
    return alphaout
    
def computeret(close,pos,backday,pnl):

    ret = close[backday+1:]/close[backday:-1]
    
    pos = (pos.T/np.sum(pos,axis = 1)).T
    pos[np.isnan(pos)]=0
    
    pnlret = np.sum(pos*ret,axis = 1)
    pnlret[pnlret==0]=1
    
    np.savetxt('test2.csv',pos,delimiter=',')   
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
    

    

def backtestalpha(startdate,enddate,changedate,subuniversepath,backday,alphatype,booksize):
    w.start()
    tdate = startdate
    j = 0
    changelist = listread(changedate)
    pnl =[booksize] 
    ret =[]
    changelist.append(enddate)
    while (tdate<= enddate) and(j<len(changelist)) :
        data = []
        codelist = w.wset("sectorconstituent","date="+tdate.strftime('%Y%m%d')+";windcode="+subuniversepath+';field= wind_code').Data[0]
        #codelist = ['000016.sh']
        datelist = [w.tdaysoffset(0-backday, tdate, "").Data[0][0].date(),w.tdaysoffset(1, changelist[j], "").Data[0][0].date()]
        for i in alphatype:
            data.append(getdatacsv(codelist,datelist,i))
        alphaout = alphatest(data,backday)
        
        #pnl.extend(computeret(data[0],alphaout,backday,pnl))
        ret.extend(computeret(data[0],alphaout,backday,pnl))
        tdate = changelist[j]
        j = j+1
    
    performance(ret)
    
    return 0

        





# config
startdate = dt.date(2019,1,1)  # minimum startdate=20100101
enddate = dt.date(2019,9,1)
changedate = 'change.csv'
backdate = 20  # number of previous days necessary for calculating today's position; e.g., if you need Tue,Wed,Thu data to calculate Fri position, set backdate=3; minimum backdate is 1
booksize = 1e7  # the total portfolio monetary size (RMB)
mode = 0  # 0 for long only without hedging; 1 for long only with futures hedging; 2 for long-short
universe = 0  # 0 for all A share; 1 for subuniverse: set subuniversepath
subuniversepath = '000016.SH'  # ZZ800 for 'zhongzheng800', HS300 for 'hushen300'
pnlpath = 'pnl.csv'  # output pnl file
positionpath = 'position.csv'  # output daily position file
tradingcost = 8e-4
futurestradingcost = 0.6e-4
alphatype = ['close','volume']
backtestalpha(startdate,enddate,changedate,subuniversepath,backdate,alphatype,booksize)
#performance()

