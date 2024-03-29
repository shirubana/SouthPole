#!/usr/bin/env python
# coding: utf-8

# # 5 - Ramp Rates Study for Solar PV
# 
# This journal starts exploring doing convolution with 1min DNI weather data, to capture the characteristics of the intermittencies/clouds: the duration, the slope of the irradiance decay, and the depth of the intermittency. The purpose of this quantification is to inform battery cycles needed for a PV-battery system.
# 
#     
#     Status: example convolution created; quantification/analysis or metrics not completed.

# In[1]:


import pandas as pd
import os
import pvlib
import csv
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 3)


# In[2]:


# Using pvlib to calculate Clear-Sky performance
pvlib.__version__


# In[3]:


weatherfile = r'IOFiles\SouthPole_2021_WeatherFile_1min.csv'
df = pd.read_csv(weatherfile, skiprows=2)
df


# In[4]:


# GET METDATA
with open(weatherfile, newline='') as f:
  reader = csv.reader(f)
  metadata_headers = next(reader)  # gets the first line
  # now do something here 
  # if first row is the header, then you can do one more next() to get the next row:
  # row2 = next(f)
  metadata_values = next(reader)  # gets the first line


# In[5]:


df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']], format="%Y-%m-%d_%H%M").dt.tz_localize(tz='Etc/GMT+3')


# In[6]:


df.set_index('datetime', inplace=True)


# In[7]:


SP = pvlib.location.Location(latitude = -89.98, longitude = -24.8, tz = 'Etc/GMT+3', altitude = 2810, name='SouthPole')
SP = SP.get_clearsky(df.index)


# In[8]:


df['dni_clearsky'] = SP.dni
df['dhi_clearsky'] = SP.dhi
df['ghi_clearsky'] = SP.ghi


# In[9]:


weeks = [g for n, g in df.groupby(pd.Grouper(freq='W'))]


# In[10]:


fig, ax = plt.subplots()

for i in range (0, len(weeks)):
    data3 = weeks[i]

    plt.plot(data3.index, data3.DNI, 'k', label='measured')
    plt.plot(data3.index,data3.dni_clearsky, label='clearssky')

    plt.legend()
    plt.xticks(rotation = 45) 
    plt.ylabel('DNI [W/m$^2$]')
    plt.title('Week'+str(i))
    plt.show()


# ## Convolution Code

# In[11]:


A=2; # amplitude
T=10;
start = -5
end = 5
step = 0.05
t2=np.arange(start, step+end, step)    # t2=np.linspace(-5,5,0.05)
step = 1
t=np.arange(start, step+end, step)
mu=0; #mean
sig=np.power(0.5,0.5); #standard deviation
#n=sig*np.random(1,11)+mu; 
h0=A*np.cos(np.pi*(t-T)/T);
h1=A*np.cos(2*np.pi*(t-T)/T);
r0_conv=np.convolve(h0,data3.DNI);
r1_conv=np.convolve(h1,data3.DNI);
plt.plot(h0, label='h0')
plt.plot(h1, label='h1')
plt.legend()
plt.ylabel('filter')
plt.figure()
plt.plot(r0_conv)
plt.ylabel('R0 conv')
plt.figure()
plt.plot(r1_conv)
plt.ylabel('R1 conv')
plt.figure()
plt.plot(data3.DNI)
plt.ylabel('DNI data');


# In[12]:


plt.plot(data3.DNI/data3.dni_clearsky)
plt.title("Normalized DNI to Clear_sky expected DNI");


# In[13]:


#Example for a Matched Filter with autogenerated data
#https://github.com/PhamMinhThuy/Basic-Radar-MultiTargets-MatchedFiltering/blob/main/Basic_Radar_MultiTargets_MatchedFiltering_v1.0.py
    
    # -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:40:44 2020
@author: minhthuy.pham
"""

import numpy as np
import scipy.linalg as la
from numpy.linalg import inv
import matplotlib.pyplot as plt
from scipy.signal import*
from numpy.fft import fft, ifft

#Matched filter
def MatchedFilter(x, fs):
    #initialize
    hf = fft(x)
    h = ifft(hf.conj())
    out = np.convolve(h,x)
    return h, out

#Input
c = 3*np.power(10,8)
td = 1*10**-6
fs = 500*np.power(10,6)
f1 = 100*np.power(10,6)
t =  np.linspace(0,td-1/fs, np.round(int(td*fs))+1)
x = chirp(t,0,td, f1)


fil = MatchedFilter(x,fs)
h = fil[0]

#Objects
n_obj = 3
dr = np.zeros(n_obj)
dr[0] = 200
dr[1] = 250
dr[2] = 261
t_dr = dr*2/c
nmax_zeros = np.zeros(n_obj)
nmax_zeros = np.round(t_dr*fs)
nmax_x = np.ma.size(x)
sig_size = int(np.amax(nmax_zeros)+ nmax_x)
x_r = np.zeros((n_obj, sig_size))
nr_out = np.linspace(0, 1/fs*(sig_size-1), sig_size)
for it in range(0,n_obj):
    x_n = x + 1*np.random.randn(nmax_x)
    x_r[it,int(nmax_zeros[it]):int(nmax_zeros[it]+nmax_x)] = x_n
sig_com = np.sum(x_r, axis = 0)
out = np.convolve(h,sig_com)

plt.figure()
plt.subplot(411)
plt.plot(np.power(10,6)*t, x)
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Chirp signal')
plt.title('Input signal, tau =%d us, Beta =%d MHz,  fs = %d MHz' %(np.power(10,6)*td, 10**-6*f1, 10**-6*fs))
plt.show()

#Return signal
plt.subplot(412)
t_r = np.linspace(0,1/fs*(sig_size -1), sig_size)
plt.plot(np.power(10,6)*t_r, x_r[0, :])
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Return chirp signal of the 1st object')

#Return signal
plt.subplot(413)
plt.plot(np.power(10,6)*t_r, x_r[1,:])
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Return chirp signal of the 2nd object')

#Return signal
plt.subplot(414)
plt.plot(np.power(10,6)*t_r, x_r[2,:])
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Return chirp signal of the 3rd object')

plt.figure()
# Output
plt.subplot(311)
plt.plot(np.power(10,6)*t_r, sig_com)
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Composite signal')
plt.show()

# Output & delay
plt.subplot(312)
nmax_out = np.ma.size(out)
n_out = np.linspace(0, 1/fs*(nmax_out-1), nmax_out)
plt.plot(np.power(10,6)*n_out, out)
plt.grid(True)
plt.xlabel('t(us)')
plt.ylabel('Output')
plt.show()

# Output & distance
plt.subplot(313)
nmax_out = np.ma.size(out)
n_out = np.linspace(0, 1/fs*(nmax_out-1), nmax_out)
dist = (n_out - td)*c/2
plt.plot(dist, out)
plt.grid(True)
plt.xlabel('Distance (m)')
plt.ylabel('Output')
plt.show()


# In[ ]:




