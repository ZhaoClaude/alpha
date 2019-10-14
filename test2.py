import numpy as np
import math
import csv
import sys
import os
import matplotlib.pyplot as plt
import datetime as dt
from WindPy import *
from alphatool import wq101 as wq

    



def listread(filename):
    return []

def getdata(codelist,datelist,atype,sub):
    filename = 'histdata\\'+sub[:6]+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv'
    if os.path.exists(filename):
        print(filename)
        data = np.loadtxt('histdata\\'+sub[:6]+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv',delimiter=',')
        return(data)        
    else:
        data = []
        for i in codelist:
            temp = w.wsd(i,atype,datelist[0],datelist[1],"PriceAdj=F").Data[0]
            data.append(temp)
        data =np.array(data).T
        print('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv')
        np.savetxt('histdata\\'+sub[:6]+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv',data,delimiter=',')
        return(data)
        
#def getdatacsv(codelist,datelist,atype,sub):
#    print('histdata\\'+atype+datelist[0].strftime('%Y%m%d')+'.csv')
#    data = np.loadtxt('histdata\\'+sub[:6]+atype+datelist[0].strftime('%Y%m%d')+'_'+datelist[1].strftime('%Y%m%d')+'.csv',delimiter=',')
#    return(data)

def gettradestatus(t1,t2):
    t3 = (t1>0) & (t2==0)
    return(t3)
    



    

def alphatest(data,backday):
    return alphatest12(data,backday);

def alphatest12(data,backday):
    close = data['close'][:-1]
    volume = data['volume'][:-1]
    

    alpha = np.sign(wq.delta(volume,backday,backday))*(-1*wq.delta(close,backday,backday))
    np.savetxt('test3.csv',alpha,delimiter=',')
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
    close = data['close'][:-1]
    vwap = data['vwap'][:-1]
    volume = data['volume'][:-1]
    t1 = wq.tsmax(vwap-close,backday)
    t2 = wq.tsmin(vwap-close,backday)
    t3 = wq.delta(volume,backday,backday)
    
    print(t1.shape,t2.shape,t3.shape)
    alpha =  (wq.rankdata(wq.tsmax(vwap-close,backday))+wq.rankdata(wq.tsmin(vwap-close,backday)))*wq.rankdata(wq.delta(volume,backday,backday))
    np.savetxt('test3.csv',alpha,delimiter=',')
    return(alpha)   

    
#    alphaout = np.zeros([data[0].shape[0]-backday-1,data[0].shape[1]])
#    for i in range(backday,len(close)-1):
#        temp = vwap[i-backday:i]-close[i-backday:i]
#        t2 = np.max(temp,axis = 0)
#        t3 = np.min(temp,axis = 0)
#        t4 = volume[i-1]-volume[i-backday]
#        alphaout[i-backday] = (wq.rankdata(t2)+wq.rankdata(t3))*wq.rankdata(t4)
        
        
    

    #alphaout = np.ones([data[0].shape[0]-backday-1,data[0].shape[1]])
    
#    return alphaout
    
def computeret(close,pos,backday,pnl,tstatus,tradingcost):
    
    pos[pos<=0] = 0
    pos[np.isnan(pos)]=0
    pos = (pos.T/np.sum(pos,axis = 1)).T
    pos[tstatus[backday:-1]==False] = 0   
    
    share = np.zeros(np.shape(close))

    spnl = np.zeros(len(close))
    rcost = np.zeros(len(close))
    spnl[backday+1] =pnl
    for i in range(backday+1,len(close)-1):


        share[i] =np.ceil(pos[i-backday-1]/close[i]*spnl[i]/100)*100
        rcost[i+1] = np.nansum(np.abs(share[i]-share[i-1])*close[i])*tradingcost
        addshare = spnl[i]-np.nansum(share[i]*close[i])
        
        spnl[i+1] = addshare+np.nansum(share[i]*close[i+1])-rcost[i+1]

    

  
    np.savetxt('test2.csv',share,delimiter=',')

    return list(spnl[backday+1::])

def performance(pnl):
   # print(pnl)
    maxprofit = 0
    maxdrawdown = 0
    pnl = np.array(pnl)/pnl[0]
    ret = (pnl[1:]/pnl[:-1])-1;
    
    for i in pnl:
        maxprofit = max(maxprofit,i)
        maxdrawdown = max([maxprofit-i,maxdrawdown])
    sharpe =np.mean(ret)/np.std(ret)*(252**0.5)
    #np.savetxt('test.csv',ret)
    print ("the final pnl is ",pnl[-1])
    print ("the maxdrawdown is",maxdrawdown)
    print("the shapre ratio is",sharpe)
    plt.plot(pnl)
    plt.show()
    

    

def backtestalpha(startdate,enddate,changedate,subuniversepath,backday,alphatype,booksize,tradingcost):
    w.start()
    tdate = startdate
    j = 0
    changelist = listread(changedate)
    pnl =[booksize] 

    changelist.append(enddate)
    while (tdate<= enddate) and(j<len(changelist)) :
        data = dict.fromkeys(alphatype)
        
        codelist = w.wset("sectorconstituent","date="+tdate.strftime('%Y%m%d')+";windcode="+subuniversepath+';field= wind_code').Data[0]
        #codelist = ['000016.sh']
        datelist = [w.tdaysoffset(0-backday-1, tdate, "").Data[0][0].date(),w.tdaysoffset(1, changelist[j], "").Data[0][0].date()]
        print(codelist)

        for i in alphatype:
            data[i] = getdata(codelist,datelist,i,subuniversepath)
        tstatus = gettradestatus(data['volume'],data['maxupordown'])
        data.pop('maxupordown')
        
        alphaout = alphatest(data,backday)
        
        #pnl.extend(computeret(data[0],alphaout,backday,pnl))
        pnl.extend(computeret(data['close'],alphaout,backday,pnl[-1],tstatus,tradingcost))
        tdate = changelist[j]
        j = j+1
    
    performance(pnl)
    
    return 0

        





# config
startdate = dt.date(2019,6,28)  # minimum startdate=20100101
enddate = dt.date(2019,9,1)
changedate = 'change.csv'
backdate = 1  # number of previous days necessary for calculating today's position; e.g., if you need Tue,Wed,Thu data to calculate Fri position, set backdate=3; minimum backdate is 1
booksize = 1e7  # the total portfolio monetary size (RMB)
mode = 0  # 0 for long only without hedging; 1 for long only with futures hedging; 2 for long-short
universe = 0  # 0 for all A share; 1 for subuniverse: set subuniversepath
subuniversepath = '000016.SH'  # ZZ800 for 'zhongzheng800', HS300 for 'hushen300'
pnlpath = 'pnl.csv'  # output pnl file
positionpath = 'position.csv'  # output daily position file
tradingcost = 1.5e-3
futurestradingcost = 0.6e-4
alphatype = ['close','volume','vwap','maxupordown']
backtestalpha(startdate,enddate,changedate,subuniversepath,backdate,alphatype,booksize,tradingcost)
#performance()

