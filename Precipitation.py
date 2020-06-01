#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import re
import urllib.request
import numpy as np
from datetime import datetime, timedelta


# In[2]:


def find_nearest_cell(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx


# In[3]:


latarray = np.linspace(-89.875,89.875,720)
lonarray = np.linspace(0.125,359.875,1440)
huancayo = (-12.06513, 360-75.20486)


# In[4]:


celllatindex = find_nearest_cell(latarray,huancayo[0])
celllonindex = find_nearest_cell(lonarray,huancayo[1])
print(celllatindex,celllonindex)


# In[5]:


zerodate = datetime(1850,1,1)
zerodate.isoformat(' ')


# In[6]:


begindate = zerodate + timedelta(days=56978.5)
begindate.isoformat(' ')


# In[7]:


enddate = zerodate + timedelta(days=89850.5)
enddate.isoformat(' ')


# In[8]:


intervals = [[0,4999],[5000,9999],[10000,14999],[15000,19999],[20000,24999],[25000,29999],[30000,34674]]

pptlist = []
daylist = []


# In[9]:


for interval in intervals:
    fp = urllib.request.urlopen("https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/NEX-GDDP/bcsd/rcp45/r1i1p1/pr/CSIRO-Mk3-6-0.ncml.ascii?pr["+str(interval[0])+":1:"+str(interval[1])+"]["+str(celllatindex)+":1:"+str(celllatindex)+"]["+str(celllonindex)+":1:"+str(celllonindex)+"]")

    
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    
    lines = mystr.split('\n')
    breakers = []
    breakerTexts = ['pr[time','pr.pr','pr.time']
    for line in lines:
        for text in breakerTexts:
            if text in line:
                breakers.append(lines.index(line))
                
    dayline = lines[breakers[0]]
    dayline = re.sub('\[|\]',' ',dayline)
    days = int(dayline.split()[4])
    print("Procesing interval %s of %d days" % (str(interval), days))
    
    for item in range(breakers[1]+1, breakers[1]+days+1):
        ppt = float(lines[item].split(',')[1])*86400
        pptlist.append(ppt)
        
    for day in lines[breakers[2]+1].split(','):
        daylist.append(zerodate + timedelta(days=float(day)))
                                
                                
                                
                


# In[10]:


plt.plot(daylist,pptlist)
plt.gcf().autofmt_xdate()
plt.ylabel('Global Precipitation (mm/day)')
plt.show()


# In[ ]:




