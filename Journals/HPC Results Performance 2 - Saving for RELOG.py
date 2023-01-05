#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


EWfile = r'TEMP\EWG_center.csv'
NSfile = r'TEMP\NSG_center.csv'


# In[3]:


EWdf = pd.read_csv(EWfile)
NSdf = pd.read_csv(NSfile)


# In[4]:


EWdf['datetime'] = pd.to_datetime(EWdf['datetime'])
NSdf['datetime'] = pd.to_datetime(NSdf['datetime'])
EWdf.set_index('datetime', inplace=True)
NSdf.set_index('datetime', inplace=True)


# In[5]:


EWdf.drop(columns=['DNI', 'DHI', 'GHI', 'temp_air', 'wind_speed', 
                   'Unnamed: 0', 'Orientation', 'Timestamp', 'solpos_zenith', 
                   'Row', 'Module',
                  'solpos_azimuth'], inplace=True)

NSdf.drop(columns=['DNI', 'DHI', 'GHI', 'temp_air', 'wind_speed', 
                   'Unnamed: 0', 'Orientation', 'Timestamp',
                   'Row', 'Module',
                  ], inplace=True)


# In[9]:


weatherfile = r'C:\Users\sayala\Documents\GitHub\Studies\SouthPole\Journals\TEMP\SouthPole_2021_WeatherFile.csv'


# In[10]:


df = pd.read_csv(weatherfile, skiprows=2)


# In[11]:


df['datetime'] = pd.to_datetime(df[['Year','Month','Day', 'Hour']], format="%Y-%m-%d_%H%M").dt.tz_localize(tz='Etc/GMT+3')
df.set_index('datetime', inplace=True)


# In[12]:


#EWdf.rename(columns={"temp_air": "Tdry", "wind_speed": "Wspd"}, inplace=True)
#NSdf.rename(columns={"temp_air": "Tdry", "wind_speed": "Wspd"}, inplace=True)


# In[13]:


result = pd.concat([df, EWdf], axis=1)
result = pd.concat([result, NSdf], axis=1)


# In[14]:


result = result.tz_convert(tz='Etc/GMT+3')


# In[15]:



#result['Row'] = 4
#result['Module'] = 10
#result.drop(columns=['Unnamed: 0'], inplace=True)
#result.drop(columns=['Orientation'], inplace=True)
#result.drop(columns=['Timestamp'], inplace=True)


# In[16]:


result.to_csv(r'TEMP\HPC_SAMFormat.csv')


# In[ ]:




