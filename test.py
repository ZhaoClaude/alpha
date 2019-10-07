from numpy import *
import math
import csv
import sys
import os
from functions import *
import matplotlib.pyplot as plt

# config
startdate = 20100101  # minimum startdate=20100101
enddate = 20141231  # maximum enddate=20141231
backdate = 1  # number of previous days necessary for calculating today's position; e.g., if you need Tue,Wed,Thu data to calculate Fri position, set backdate=3; minimum backdate is 1
booksize = 1e7  # the total portfolio monetary size (RMB)
mode = 1  # 0 for long only without hedging; 1 for long only with futures hedging; 2 for long-short
universe = 0  # 0 for all A share; 1 for subuniverse: set subuniversepath
subuniversepath = 'ZZ800.csv'  # ZZ800 for 'zhongzheng800', HS300 for 'hushen300'
pnlpath = 'pnl.csv'  # output pnl file
positionpath = 'position.csv'  # output daily position file
tradingcost = 8e-4
futurestradingcost = 0.6e-4

# import basedata
subuniverse = file2series(subuniversepath)
subuniverse = np.array([int(x) for x in subuniverse])

parent_path = 'D:\\morgan\\v1.0'
basedata = os.path.join(parent_path, 'basedata')
# fundamental=os.path.join(parent_path,'fundamental')
# WINDdata=os.path.join(parent_path,'WINDdata')
buyvalid = file2mat(os.path.join(basedata, 'buyshare.csv'), universe, subuniverse)
sellvalid = file2mat(os.path.join(basedata, 'sellshare.csv'), universe, subuniverse)
dates = file2series(os.path.join(basedata, 'dates_is.csv'))
stocklist = file2liststring(os.path.join(basedata, 'stocklist.csv'), universe, subuniverse)
# ret= file2mat('ret.csv',universe,subuniverse)
cps = file2mat(os.path.join(basedata, 'ashare_close.csv'), universe, subuniverse)
ms = file2mat(os.path.join(basedata, 'ms.csv'), universe, subuniverse)
if mode == 1:
    fcps = file2series(os.path.join(basedata, 'futures_close.csv'))
else:
    fcps = []
ret = file2mat(os.path.join(basedata, 'return.csv'), universe, subuniverse)
beta = file2list(os.path.join(basedata, 'beta1.csv'), universe, subuniverse)
fret = file2series(os.path.join(basedata, 'futures_ret.csv'))

[instrumentsize, datesize, startdi, enddi] = initialize(backdate, startdate, enddate, ms, dates)

# import custom data
# ptgtime = file2mat(os.path.join(WINDdata,'targetpricenextavg_weightedbytime.csv'),universe,subuniverse)
open = file2mat(os.path.join(basedata, 'open.csv'), universe, subuniverse)
# sales= file2mat(os.path.join(fundamental,'sales.csv'),universe,subuniverse)
industry = file2list(os.path.join(basedata, 'industry.csv'), universe, subuniverse)
industry = np.array([int(x) for x in industry])

# strategy start

# sample 1 start
alpha = [];
alpha = np.loadtxt("alpha.csv", delimiter=",");
print
shape(alpha)
print
datesize;
print
startdi;
print
enddi;

performance(datesize, instrumentsize, startdi, enddi, alpha, booksize, cps, mode, fcps, buyvalid, sellvalid, ms,
            tradingcost, futurestradingcost, pnlpath, positionpath, dates, stocklist, ret, fret, beta)


