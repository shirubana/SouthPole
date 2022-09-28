#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import pvlib


# In[2]:


pvlib.__version__


# In[3]:


weatherfolder = r'WeatherFileDats'


# In[4]:


# NOAO  -- pvlib / SAM
# dw_solar = ghi
# direct_n = dni
# diffuse = dhi
# rh = 
# pressure
# windspd = wind_speed
# windir
# tmep = temp_air

headers = ['year', 'jday', 'month', 'day', 'hour', 'minute', 'dt', 'zen',
'ghi', 'blank', 'uw_solar', 'blank', 'dni', 'blank', 'dhi', 'blank',
'dw_ir', 'blank', 'dw_casetemp', 'blank', 'dw_dometemp', 'blank', 'uw_ir',
'blank', 'uw_casetemp', 'blank', 'uw_dometemp', 'blank', 'uvb', 'blank', 'par',
'blank', 'netsolar', 'blank', 'netir', 'blank', 'totalnet', 'blank', 'temp_air',
'blank', 'rh', 'blank', 'wind_speed', 'blank', 'winddir', 'blank', 'pressure', 'blank'
]


# In[5]:


df_all = pd.DataFrame()
for ii in range (1, 366):
    wfile = os.path.join(weatherfolder, 'spo21{:2}.dat'.format(f'{ii:03}'))
    df = pd.read_table(wfile, sep="\s+", skiprows=2, header=None,  engine='python') #, sep="\s+") 
    df.columns=headers
    df = df.drop(columns='blank')
    frames = [df_all, df]
    df_all = pd.concat(frames)


# In[6]:


df_all['timestamps'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour', 'minute']])


# In[7]:


df_all.set_index(df_all['timestamps'], inplace = True)


# In[8]:


df_all = df_all.iloc[:-60]


# In[9]:


df_all.replace(to_replace = -9999.9, value =0 , inplace=True)# -9999.9]


# In[10]:


#df_all['dhi'].replace(to_replace = -0.1, value =0 , inplace=True)# -9999.9]


# In[11]:


df_all.loc[df_all['dni']<0,'dni']=0
df_all.loc[df_all['ghi']<0,'ghi']=0
df_all.loc[df_all['dhi']<0,'dhi']=0


# In[12]:


df_all.replace(to_replace = -9999.9, value =0 , inplace=True)# -9999.9]-0.1


# In[13]:


metdata = {'latitude':  -89.98,  # From the NOAA metdata
           'longitude':-24.80,
           'source':'NOAA',
           'elevation': 2810,
            'TZ':-3}


# In[14]:


pvlib.iotools.saveSAM_WeatherFile(df_all, metdata, savefile='SAM_SP_WeatherFile.csv')


# In[ ]:




