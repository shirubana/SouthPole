#!/usr/bin/env python
# coding: utf-8

# ## Join Weather Data (DNI, DHI, WSPD, ETC)

# In[1]:


import bifacial_radiance
import numpy as np


# In[2]:


import os
from pathlib import Path
import pandas as pd

testfolder = 'TEMP' 
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[3]:


weathefile = r'C:\Users\sayala\Documents\GitHub\Studies\SouthPole\Journals\TEMP\SouthPole_2021_WeatherFile.csv'
weatherfile = r'C:\Users\sayala\Documents\GitHub\Studies\SouthPole\Journals\IOFiles\POWER_Point_Hourly_20160101_20161231_090d00S_000d00E_LT.csv'


# In[4]:


demo = bifacial_radiance.RadianceObj('SD',str(testfolder))  
# Read in the weather data pulled in above. 
metdata = demo.readWeatherFile(weatherfile, source='SAM', coerce_year=2016) 


# In[5]:


foo2 = pd.DataFrame()
foo2['DNI'] = metdata.dni
foo2['DHI'] = metdata.dhi
foo2['GHI'] = metdata.ghi
foo2['temp_air'] = metdata.temp_air
foo2['wind_speed'] = metdata.wind_speed
foo2['solpos_zenith'] = metdata.solpos.zenith.values
foo2['solpos_azimuth'] = metdata.solpos.azimuth.values
foo2['datetime'] = metdata.datetime
#foo2.set_index(foo2.datetime, inplace= True)


# In[6]:


df = pd.read_csv(r'C:\Users\sayala\Documents\GitHub\Studies\SouthPole\Journals\TEMP\Compiled.csv')


# In[7]:


uniquetimes = df['Timestamp'].unique()


# In[8]:


uniquetimes[-93:-1]


# In[9]:


uuu = len(uniquetimes)-93


# In[10]:


uniquetimes = uniquetimes[:uuu]


# In[11]:


df['DNI'] = np.nan
df['DHI'] = np.nan
df['GHI'] = np.nan
df['temp_air'] = np.nan
df['wind_speed'] = np.nan
df['solpos_zenith'] = np.nan
df['solpos_azimuth'] = np.nan
df['datetime'] = np.nan


for ii in range (0, len(uniquetimes)):
    df.loc[df.Timestamp == uniquetimes[ii],'DNI'] = foo2.loc[uniquetimes[ii]].DNI
    df.loc[df.Timestamp == uniquetimes[ii],'DHI'] = foo2.loc[uniquetimes[ii]].DHI
    df.loc[df.Timestamp == uniquetimes[ii],'GHI'] = foo2.loc[uniquetimes[ii]].GHI
    df.loc[df.Timestamp == uniquetimes[ii],'temp_air'] = foo2.loc[uniquetimes[ii]].temp_air
    df.loc[df.Timestamp == uniquetimes[ii],'wind_speed'] = foo2.loc[uniquetimes[ii]].wind_speed
    df.loc[df.Timestamp == uniquetimes[ii],'solpos_zenith'] = foo2.loc[uniquetimes[ii]].solpos_zenith
    df.loc[df.Timestamp == uniquetimes[ii],'solpos_azimuth'] = foo2.loc[uniquetimes[ii]].solpos_azimuth
    df.loc[df.Timestamp == uniquetimes[ii],'datetime'] = foo2.loc[uniquetimes[ii]].datetime
    df.loc[df.Timestamp == uniquetimes[ii],'datetime'] = foo2.loc[uniquetimes[ii]].datetime


# In[38]:


df['DNI'] = np.nan
df['DHI'] = np.nan
df['GHI'] = np.nan
df['temp_air'] = np.nan
df['wind_speed'] = np.nan
df['solpos_zenith'] = np.nan
df['solpos_azimuth'] = np.nan
df['datetime'] = np.nan


for ii in range (0, 25):
    df.loc[df.Timestamp == uniquetimes[ii],'DNI'] = foo2.loc[uniquetimes[ii]].DNI
    df.loc[df.Timestamp == uniquetimes[ii],'DHI'] = foo2.loc[uniquetimes[ii]].DHI
    df.loc[df.Timestamp == uniquetimes[ii],'GHI'] = foo2.loc[uniquetimes[ii]].GHI
    df.loc[df.Timestamp == uniquetimes[ii],'temp_air'] = foo2.loc[uniquetimes[ii]].temp_air
    df.loc[df.Timestamp == uniquetimes[ii],'wind_speed'] = foo2.loc[uniquetimes[ii]].wind_speed
    df.loc[df.Timestamp == uniquetimes[ii],'solpos_zenith'] = foo2.loc[uniquetimes[ii]].solpos_zenith
    df.loc[df.Timestamp == uniquetimes[ii],'solpos_azimuth'] = foo2.loc[uniquetimes[ii]].solpos_azimuth
    df.loc[df.Timestamp == uniquetimes[ii],'datetime'] = foo2.loc[uniquetimes[ii]].datetime
    df.loc[df.Timestamp == uniquetimes[ii],'datetime'] = foo2.loc[uniquetimes[ii]].datetime


# ## Separate into NS and EW dataframes

# In[12]:


NSG = df.loc[df.Orientation == 'NS'].copy()
EWG = df.loc[df.Orientation == 'EW'].copy()
NSG.head(1)


# ## Sort Values by Date, Row and Module

# In[13]:


NSG = NSG.sort_values(['Timestamp', 'Row', 'Module'],
              ascending = [True, True, True])
EWG = EWG.sort_values(['Timestamp', 'Row', 'Module'],
              ascending = [True, True, True])


# In[14]:


from ast import literal_eval


# In[15]:


NSG.Wm2Back = NSG.Wm2Back.apply(literal_eval)


# In[16]:


NSG.Wm2Front = NSG.Wm2Front.apply(literal_eval)


# In[17]:


EWG.Wm2Back = EWG.Wm2Back.apply(literal_eval)


# In[18]:


EWG.Wm2Front = EWG.Wm2Front.apply(literal_eval)


# In[19]:


NSG.head(1)


# ## Calculate POAs

# In[20]:


Wm2Front = pd.DataFrame(item for item in NSG['Wm2Front'])
Wm2Back = pd.DataFrame(item for item in NSG['Wm2Back'])

NSG['SouthFacing_POA'] = (Wm2Front+Wm2Back*0.6).min(axis=1).values
NSG['NorthFacing_POA'] = (Wm2Front*0.6+Wm2Back).min(axis=1).values
NSG.SouthFacing_POA

Wm2Front = pd.DataFrame(item for item in EWG['Wm2Front'])
Wm2Back = pd.DataFrame(item for item in EWG['Wm2Back'])
EWG['EastFacing_POA'] = (Wm2Front+Wm2Back*0.6).min(axis=1).values
EWG['WestFacing_POA'] = (Wm2Front*0.6+Wm2Back).min(axis=1).values


# ## Asign CEC module 

# In[21]:


import pvlib 
CECMODS = pvlib.pvsystem.retrieve_sam('CECMod')
INVERTERS = pvlib.pvsystem.retrieve_sam('CECInverter')

CECMOD_CSI = CECMODS['LONGi_Green_Energy_Technology_Co___Ltd__LR6_72HBD_380M']


# In[22]:


# [col for col in CECMODS if col.startswith('LONGi') & col.endswith('400M')]


# In[23]:


CECMOD_CSI = CECMODS['LONGi_Green_Energy_Technology_Co___Ltd__LR6_72HBD_380M']
CECMOD_CSI


# ## Calculate Performances

# In[24]:


NSG['North_Performance'] = bifacial_radiance.performance.calculatePerformance(effective_irradiance = NSG['NorthFacing_POA'], CECMod = CECMOD_CSI,
                                                  temp_air = NSG['temp_air'],
                                                  wind_speed = NSG['wind_speed'],
                                                  glassglass=True)

NSG['South_Performance'] = bifacial_radiance.performance.calculatePerformance(effective_irradiance = NSG['SouthFacing_POA'], CECMod = CECMOD_CSI,
                                                  temp_air = NSG['temp_air'],
                                                  wind_speed = NSG['wind_speed'],
                                                  glassglass=True)

EWG['East_Performance'] = bifacial_radiance.performance.calculatePerformance(effective_irradiance = EWG['EastFacing_POA'], CECMod = CECMOD_CSI,
                                                  temp_air = EWG['temp_air'],
                                                  wind_speed = EWG['wind_speed'],
                                                  glassglass=True)

EWG['West_Performance'] = bifacial_radiance.performance.calculatePerformance(effective_irradiance = EWG['WestFacing_POA'], CECMod = CECMOD_CSI,
                                                  temp_air = EWG['temp_air'],
                                                  wind_speed = EWG['wind_speed'],
                                                  glassglass=True)


# In[25]:


NSG.keys()


# In[26]:


NSG.loc[0]


# In[27]:


foo = NSG[['Timestamp', 'Row', 'Module', 'Orientation', 'DNI', 'DHI',
       'GHI', 'temp_air', 'wind_speed', 'solpos_zenith', 'solpos_azimuth',
       'datetime', 'SouthFacing_POA', 'NorthFacing_POA',
       'North_Performance', 'South_Performance']]


# In[28]:


foo['datetime'] = pd.to_datetime(foo['datetime'], format="%Y-%m-%d_%H%M").dt.tz_convert(tz='Etc/GMT-14')


# In[29]:


foo.to_csv('NSG_2016.csv')


# In[30]:


foo = EWG[['Timestamp', 'Row', 'Module', 'Orientation', 'DNI', 'DHI',
       'GHI', 'temp_air', 'wind_speed', 'solpos_zenith', 'solpos_azimuth',
       'datetime', 'EastFacing_POA', 'WestFacing_POA',
       'East_Performance', 'West_Performance']]


# In[31]:


foo['datetime'] = pd.to_datetime(foo['datetime'], format="%Y-%m-%d_%H%M").dt.tz_convert(tz='Etc/GMT-14')


# In[32]:


foo.to_csv('EWG_2016.csv')


# In[33]:


NSG_center = NSG.loc[(NSG.Row == 4) & (NSG.Module == 10) ].copy()
EWG_center = EWG.loc[(EWG.Row == 4) & (EWG.Module == 10) ].copy()


# In[34]:


foo = NSG_center[['Timestamp', 'Row', 'Module', 'Orientation', 'DNI', 'DHI',
       'GHI', 'temp_air', 'wind_speed', 'solpos_zenith', 'solpos_azimuth',
       'datetime', 'SouthFacing_POA', 'NorthFacing_POA',
       'North_Performance', 'South_Performance']]
foo['datetime'] = pd.to_datetime(foo['datetime'], format="%Y-%m-%d_%H%M").dt.tz_convert(tz='Etc/GMT-14')
foo.to_csv('NSG_center_2016.csv')

foo = EWG_center[['Timestamp', 'Row', 'Module', 'Orientation', 'DNI', 'DHI',
       'GHI', 'temp_air', 'wind_speed', 'solpos_zenith', 'solpos_azimuth',
       'datetime', 'EastFacing_POA', 'WestFacing_POA',
       'East_Performance', 'West_Performance']]
foo['datetime'] = pd.to_datetime(foo['datetime'], format="%Y-%m-%d_%H%M").dt.tz_convert(tz='Etc/GMT-14')
foo.to_csv('EWG_center_2016.csv')


# In[35]:


# UGLY MAPPING

#x=range(0,len(NSG['NorthFacing_POA']))
#plt.figure(figsize=(18, 6), dpi=80)

#plt.plot(x,  NSG['NorthFacing_POA'], label='North')
#plt.plot(x, NSG['SouthFacing_POA'], label='South')
#x=range(0,len(EWG['EastFacing_POA']))
#plt.plot(x,  EWG['EastFacing_POA'], label='East')
#plt.plot(x, EWG['WestFacing_POA'], 'y', label='West')
#plt.plot(range(45,80), np.ones(80-45)*1286, '.r', label='VF SouthFacing')
#plt.plot(range(85,120), np.ones(120-85)*1495,  '.r')
#plt.plot(range(120,160), np.ones(160-120)*1664,  '.r')
#plt.plot(range(165,190), np.ones(190-165)*1602, '.r')
#plt.plot(range(200,240), np.ones(240-200)*1470, '.r')
#plt.plot(range(250,280), np.ones(280-250)*1193, '.r')
#plt.plot(range(290,310), np.ones(310-290)*531, '.r')
#plt.plot(range(320,360), np.ones(360-320)*449, '.r')
#plt.ylabel("Irradiance [W/m$^2$]")
#plt.legend(loc='lower center', ncol=3)


# ## WORKING WITH 2021-02-21_0200

# In[36]:


Wm2Front = pd.DataFrame(item for item in NSG[NSG['Timestamp'] == '2016-12-21_0500']['Wm2Front'])
Wm2Back = pd.DataFrame(item for item in NSG[NSG['Timestamp'] == '2016-12-21_0500']['Wm2Back'])
SouthF = (Wm2Front+Wm2Back*0.6)
NorthF = (Wm2Front*0.6+Wm2Back)

Wm2Front = pd.DataFrame(item for item in EWG[EWG['Timestamp'] == '2016-12-21_0500']['Wm2Front'])
Wm2Back = pd.DataFrame(item for item in EWG[EWG['Timestamp'] == '2016-12-21_0500']['Wm2Back'])
EastF = (Wm2Front+Wm2Back*0.6)
WestF = (Wm2Front*0.6+Wm2Back)


# In[37]:


ii = 0
arrayallN = pd.DataFrame()
arrayallS = pd.DataFrame()
arrayallE = pd.DataFrame()
arrayallW = pd.DataFrame()

for rr in range (0, 5):
    rowallN = pd.DataFrame()
    rowallS = pd.DataFrame()
    rowallE = pd.DataFrame()
    rowallW = pd.DataFrame()

    for mm in range (0, 5):
        # North
        my_list = NorthF.loc[ii]
        my_list = pd.DataFrame(np.array(my_list).reshape(6,9)).T
        rowallN = pd.concat([rowallN, my_list], axis=1)
        # South
        my_list = SouthF.loc[ii]
        my_list = pd.DataFrame(np.array(my_list).reshape(6,9)).T
        rowallS = pd.concat([rowallS, my_list], axis=1)
        # East
        my_list = EastF.loc[ii]
        my_list = pd.DataFrame(np.array(my_list).reshape(6,9)).T
        rowallE = pd.concat([rowallE, my_list], axis=1)
        # West
        my_list = WestF.loc[ii]
        my_list = pd.DataFrame(np.array(my_list).reshape(6,9)).T
        rowallW = pd.concat([rowallW, my_list], axis=1)
        ii += 1
    arrayallN = pd.concat([arrayallN, rowallN], axis=0, sort=False, ignore_index=True)
    arrayallS = pd.concat([arrayallS, rowallS], axis=0, sort=False, ignore_index=True)
    arrayallE = pd.concat([arrayallE, rowallE], axis=0, sort=False, ignore_index=True)
    arrayallW = pd.concat([arrayallW, rowallW], axis=0, sort=False, ignore_index=True)


# In[ ]:


maxmax = np.max([arrayallN.max().max(),
arrayallS.max().max(),
arrayallE.max().max(),
arrayallW.max().max()])

minmin = np.min([arrayallN.min().min(),
arrayallS.min().min(),
arrayallE.min().min(),
arrayallW.min().min()])

print("Max Irradiance in the 4 arrays: ", np.round(maxmax))
print("Min Irradiance in the 4 arrays: ", np.round(minmin))


# In[ ]:


# Printing POA_t (Gfront + Grear*bifaciality)) on each Cell

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)

df = arrayallN

with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect = 0.4)
    plt.colorbar(label='POA Irradiance W/m$^2}$')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("North")    
plt.show()

plt.figure()

df = arrayallS


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect = 0.4)
    plt.colorbar(label='POA Irradiance W/m$^2}$')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("South")        
plt.show()

plt.figure()

df = arrayallE


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect = 0.4)
    plt.colorbar(label='POA Irradiance W/m$^2}$')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("East")        
plt.show()

plt.figure()

df = arrayallW

with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect = 0.4)
    plt.colorbar(label='POA Irradiance W/m$^2}$')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("West")        
plt.show()


# # MAP PERFORMANCES

# In[ ]:


ii = 0
PowerallN = []
PowerallS = []
PowerallE = []
PowerallW = []

for rr in range (0, 4):
    rowallN = []
    rowallS = []
    rowallE = []
    rowallW = []

    for mm in range (0, 10):
        ii += 1
        rowallN.append(NSG['North_Performance'].iloc[ii])
        rowallS.append(NSG['South_Performance'].iloc[ii])
        rowallE.append(EWG['East_Performance'].iloc[ii])
        rowallW.append(EWG['West_Performance'].iloc[ii])

    PowerallN.append(rowallN)
    PowerallS.append(rowallS)
    PowerallE.append(rowallE)
    PowerallW.append(rowallW)

PowerallN = pd.DataFrame(PowerallN)
PowerallS = pd.DataFrame(PowerallS)
PowerallE = pd.DataFrame(PowerallE)
PowerallW = pd.DataFrame(PowerallW)


# In[ ]:


A = [PowerallN.max().max(),
PowerallS.max().max(),
PowerallE.max().max(),
PowerallW.max().max()]

B = [PowerallN.min().min(),
PowerallS.min().min(),
PowerallE.min().min(),
PowerallW.min().min()]

print("Power Mismatch in each array", np.round(np.subtract(A, B)*100/A), '%')
print("Max Module Power in each array", np.round(A), 'W')
print("Min Module Power in each array", np.round(B), 'W')


# In[ ]:


nameplate_array = 300*40
print("Power Array Nameplate ", np.round(nameplate_array/1000,1), " kW")
print("Power Array N S E W ", np.round(np.multiply(B,40/1000),1), " kW")
print("PR Array N S E W", np.round(np.multiply(B,40/nameplate_array),2))


# In[ ]:


# Printing Timestamp Data
print(NSG.iloc[30]['Timestamp'])
print("--------------------------")
print("solpos_zenith", np.round(NSG.iloc[0]['solpos_zenith'],1))
print("solpos_azimuth", np.round(NSG.iloc[0]['solpos_azimuth'],1))
print("DNI", np.round(NSG.iloc[0]['DNI'],1))
print("DHI", np.round(NSG.iloc[0]['DHI'],1))
print("GHI", np.round(NSG.iloc[0]['GHI'],1))
print("wind_speed", np.round(NSG.iloc[0]['wind_speed'],1))
print("temp_air", np.round(NSG.iloc[0]['temp_air'],1))


# In[ ]:


# Plotting Performance
df = PowerallN
maxmax = np.max(A)
minmin = np.min(B)

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect = 1.5)
    plt.colorbar(label='Power [W/m$^2$]')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("North")   
plt.show()

plt.figure()

df = PowerallS

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect =  1.5)
    plt.colorbar(label='Power [W/m$^2$]')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("South")   

plt.show()

plt.figure()

df = PowerallE

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect =  1.5)
    plt.colorbar(label='Power [W/m$^2$]')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("East")   

plt.show()

plt.figure()

df = PowerallW

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


with sns.axes_style("white"):
    fig = plt.imshow(df, cmap='hot', vmin=minmin, vmax=maxmax, interpolation='none', aspect =  1.5)
    plt.colorbar(label='Power [W/m$^2$]')
    #plt.title('Yearly Bifacial, in matrix form')
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
plt.title("West")   
plt.show()


# In[ ]:





# In[ ]:




