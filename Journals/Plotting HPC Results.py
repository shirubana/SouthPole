#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px


dffile = r'TEMP\HPC_SAMFormat.csv'

df = pd.read_csv(dffile)


# In[2]:


df.set_index('datetime', inplace=True)


# In[3]:


df.keys()


# In[4]:


fig = px.line(df, x=df.index, y=["DNI", 'DHI', 'GHI'])
fig.show()


# In[21]:


fig = px.line(df, x=df.index, y=["North_Performance", "East_Performance", "South_Performance", "West_Performance"])
fig.show()


# In[26]:


fig = px.histogram(df, x=df.index, y="North_Performance", histfunc="avg", title="Histogram on Date Axes")
fig.update_traces(xbins_size="M1")


# In[29]:





# In[30]:


df['NSEW_Performance'] = df[["North_Performance", "East_Performance", "South_Performance", "West_Performance"]].sum(axis=1)


# In[45]:


fig = px.line(df, x=df.index, y='NSEW_Performance')
fig.show()


# In[33]:


df['NSEW_PR'] = df['NSEW_Performance']/(1200)


# In[44]:


fig = px.histogram(df, x=df.index, y="NSEW_PR", histfunc="avg", title="Histogram on Date Axes")
fig.update_traces(xbins_size="M1")


# In[ ]:




