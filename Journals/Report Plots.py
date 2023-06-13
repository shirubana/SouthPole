#!/usr/bin/env python
# coding: utf-8

# In[1]:


performancePOAresults = r'TEMP/HPC_SAMFormat_2016_bfill_noFeb29.csv'


# In[2]:


import pandas as pd


# In[3]:


data = pd.read_csv(performancePOAresults)


# In[4]:


data.set_index(pd.to_datetime(data.datetime), inplace=True)


# In[5]:


import matplotlib.pyplot as plt


# In[6]:


df = data.resample('D').mean()


# In[7]:


df


# In[8]:


df = df.drop('2016-02-29 00:00:00+14:00')


# In[9]:


partB = pd.to_datetime({
    'year': 2017,
    'month': df[df.index<'2016-05-31'].index.month,
    'day': df[df.index<'2016-05-31'].index.day})


# In[10]:


shiftyear = df[df.index<'2016-05-31'].set_index(partB)
shiftyear


# In[11]:


shiftyear.index = shiftyear.index.tz_localize(tz='Etc/GMT-14')


# In[12]:


shiftyear['North_Performance']


# In[13]:


df['North_Performance']


# In[16]:


result = pd.concat([df, shiftyear], axis=0)
result.set_index(pd.to_datetime(result.index, utc=True), inplace=True)
result.index = result.index.tz_convert(tz='Etc/GMT-14')


# In[39]:


result['4Directions'] = (result['East_Performance'] + result['West_Performance'] +
                         result['South_Performance'] + result['North_Performance'])


# In[41]:


len(result[result.index>'2016-09-22']['4Directions'])


# In[52]:


import numpy as np


# In[58]:


foo = result[result.index>'2016-09-22']
x = np.arange(0, 200)

plt.plot(x, foo['4Directions'][0:200])
#plt.margins(0)
plt.xlim([0, 180])


# In[94]:


foo.iloc[180]


# In[128]:


foo = result[result.index>'2016-09-22']
x = np.arange(0, 200)

NominalPower= 380.694*4
fig, ax = plt.subplots(figsize=(10, 6), dpi=80)
ax.plot(x, foo['4Directions'][0:200]/NominalPower)
#plt.margins(0)
ax.set_xlim([0, 180])
ax2 = ax.secondary_xaxis('top')
ax2.tick_params(axis='x')
ax2.set_xticks([0, 8, 39, 69, 100, 131, 159, 180], minor=False),
#ax2.grid(color='red')
ax.axvline(8, color='0.8')# , linestyle='--')
ax.axvline(39, color='0.8')# , linestyle='--')
ax.axvline(69, color='0.8')# , linestyle='--')
ax.axvline(100, color='0.8')# , linestyle='--')
ax.axvline(131, color='0.8')# , linestyle='--')
ax.axvline(159, color='0.8')# , linestyle='--')
ax.axvline(180, color='0.8')# , linestyle='--')

labels = [item.get_text() for item in ax2.get_xticklabels()]
newlabels = ['SEPT\n22', 'OCT. 1', 'NOV. 1', 'DEC. 1', 'JAN. 1', 'FEB. 1', 'MAR. 1', 'MAR. 22']
ax2.set_xticklabels(newlabels);
ax.set_xlabel('DAYS AFTER SEPT. 22 EQUINOX')
ax.set_ylabel('Normalized Power Output\nfor N-E-S-W System')


# In[129]:


#df.rolling(window=5, min_periods=3).sum().dropna().resample('3D').last() 

