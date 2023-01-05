#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pvlib
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


testfolder = r'WeatherFilesNASA'


# In[3]:


filelist = sorted(os.listdir(testfolder))


# In[4]:


tmydata = pd.DataFrame()

for ii in range (0, len(filelist)):

    SAMfile = os.path.join(testfolder, filelist[ii])
    
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

    #data.rename(columns={'Tdry':'DryBulb'}, inplace=True) 
    tmydata = pd.concat([tmydata, data], sort=False)


# In[5]:


print(len(data))    # 1 year data
print(len(tmydata)) # All years data


# In[6]:


smalltmy = tmydata[~tmydata['dni'].isna()]
smalltmy = smalltmy.drop(columns='snow') # Droping snow column, it's all Nans


# In[7]:


mindni = pd.DataFrame()

for ii in range(0,len(data)):
    foo = smalltmy[(smalltmy['month']==data['month'][ii]) & (smalltmy['day']==data['day'][ii]) & (smalltmy['hour']==data['hour'][ii])]
    asdf = foo.loc[foo['dni'].idxmin()]
    asdf = asdf.to_frame().T
    mindni = pd.concat([mindni, asdf])


# In[8]:


meta2


# In[9]:


metdata = {'latitude':  '-90.0',  # From the NOAA metdata
           'longitude':-0.0,
           'source':'NASA',
           'elevation': 2811.04,
            'tz':14}


# In[10]:


# Rename for SAM
mindni.rename(columns={"wspd": 'wind_speed'}, inplace=True)
mindni.rename(columns={"tdry": 'temp_air'}, inplace=True)


# In[11]:


mindni['year'] = 2021  # Not really useful, as the weather file saves based on the index year
mindni['minute'] = 0  # Not really useful, as the weather file saves based on the index year


# In[12]:


mindni


# In[13]:


pvlib.iotools.write_sam(mindni, metdata, savefile=r'TEMP\SAM_MinTMY_DNI_WeatherFile_Realyear.csv', standardSAM=False)


# In[14]:


# Replacing with 2021 so it's easier to plot/analyse
mindni['datetime'] = pd.to_datetime(mindni[['year', 'month', 'day', 'hour', 'minute']], format="%Y-%m-%d_%H%M").dt.tz_localize(tz=tz)
mindni.set_index('datetime', inplace=True)
pvlib.iotools.write_sam(mindni, metdata, savefile=r'TEMP\SAM_MinTMY_DNI_WeatherFile_2021.csv', standardSAM=False)


# In[15]:


data = mindni.copy()

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (12, 4)

plt.plot(data['dni'], 'r')
plt.ylabel('DNI Irradiance [W/m$^2$]')
plt.ylim([0, 1200])
plt.figure()
plt.plot(data['dhi'], 'g')
plt.ylabel('DHI Irradiance [W/m$^2$]')
plt.ylim([0, 1200])
plt.figure()
plt.plot(data['ghi'], 'b')
plt.ylabel('GHI Irradiance [W/m$^2$]')
plt.ylim([0, 1200])

