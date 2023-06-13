#!/usr/bin/env python
# coding: utf-8

# # NASA Min-MeteorologicalYear 
# 
# Calculates two-week minimum DNI to create a Minimum TMY 
# 
# Uses NASA data files for ~20 years

# In[1]:


import pvlib
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[7]:


SAMfile = r'../DATA/WeatherFilesNASA/POWER_Point_Hourly_20160101_20161231_090d00S_000d00E_LT.csv'


# In[9]:


with open(SAMfile) as myfile:
    head = next(myfile)#
    meta = next(myfile)

meta2=meta.split(',')
meta2[-1] = meta2[-1][:-1] # Remove the carryover sig

head2 = head.split(',')
head2[-1] = head2[-1][:-1] 

res = {head2[i]: meta2[i] for i in range(len(head2))}


data = pd.read_csv(SAMfile, skiprows=2)

metadata = {}
metadata['TZ'] = float(res['Time Zone'])
metadata['latitude'] = float(res['Latitude'])
metadata['longitude'] = float(res['Longitude'])
metadata['altitude'] = float(res['Elevation'])
metadata['city'] = res['Source']

if 'Minute' in data.columns:
    dtidx = pd.to_datetime(
        data[['year', 'month', 'day', 'hour', 'minute']])
else: 
    dtidx = pd.to_datetime(
        data[['year', 'month', 'day', 'hour']])
# in USA all timezones are integers
tz = 'Etc/GMT%+d' % -metadata['TZ']
data.index = pd.DatetimeIndex(dtidx).tz_localize(tz)


# In[10]:


data


# In[12]:


metadata


# In[13]:


import pvlib


# In[57]:


#SP = pvlib.location.Location(latitude = -89.98, longitude = -24.8, tz = 'Etc/GMT+3', altitude = 2810, name='SouthPole')
SP = pvlib.location.Location(latitude = metadata['latitude'], longitude = metadata['longitude'], tz = metadata['TZ'], 
                             altitude = metadata['altitude'], name='SouthPole')


# In[32]:


sun = SP.get_solarposition(data.index)
data['Solar_Azimuth'] = sun['azimuth']
data['Solar_Elevation'] = sun['elevation']


# In[58]:


SP = SP.get_clearsky(data.index)
data['dni_clearsky'] = SP.dni
data['dhi_clearsky'] = SP.dhi
data['ghi_clearsky'] = SP.ghi


# In[27]:


import matplotlib.pyplot as plt


# In[61]:


foo = data[data['Solar_Elevation']>0]


# In[62]:


plt.plot(data['Solar_Azimuth'])


# In[63]:


NS = foo[(foo['Solar_Azimuth'] < 90) | (foo['Solar_Azimuth'] > 270)]
EW = foo[(foo['Solar_Azimuth'] >= 90) & (foo['Solar_Azimuth'] <= 270)]


# In[71]:


NS.dni.sum()/EW.dni.sum()


# In[72]:


NS.dni_clearsky.sum()/EW.dni_clearsky.sum()

