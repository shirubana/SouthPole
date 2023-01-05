#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
from pathlib import Path
import bifacial_radiance
import bifacialvf
print(bifacialvf.__version__)
print(bifacial_radiance.__version__)


# In[2]:


testfolder = r'TEMP\SP2_02_21'
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[3]:


# LOOP
pitchs = [8] #, 3, 5] 
CHs = [0.6] #, 0.5, 0.75, 1.0]
albedo = 0.72 #, 0.8]
locs = [722740] #, 727930 ]
locsnames = ['Tucson'] #, 'Seattle']


# In[9]:


weatherfile = r'C:\Users\sayala\Documents\GitHub\Studies\SouthPole\Journals\SouthPole_2021_WeatherFile.csv'


# In[5]:


demo = bifacial_radiance.RadianceObj('Sim', path=testfolder)  


# In[6]:


#metdata = demo.readWeatherFile(weatherfile, starttime=idx, endtime=idx, source='SAM')  


# In[10]:


cumulativesky = False
startdate = ['12_21_12', '02_21_12']# , '06_21', '12_21']
startdate = ['12_21_11', '12_21_14', '12_21_17', '12_21_20', '12_21_18','12_21_23', '12_21_05', '12_21_02']# , '06_21', '12_21']
startdate = ['02_21_11', '02_21_14', '02_21_17', '02_21_20', '02_21_18','12_21_23', '02_21_05', '02_21_02']# , '06_21', '12_21']
sazmNS = 180
sazmEW = 90
limit_angle = 120
rowsWanted = [1,2,3,4,5]
modsWanted = [1,2,5,8,9]

for dd in range (0, len(startdate)):
        for zz in range(0, len(CHs)):
            for ww in range(0, len(pitchs)):

                    clearance_height = CHs[zz]
                    pitch = pitchs[ww]
                    gcr = 2/pitch
                    sdt = startdate[dd]
                    metdata = demo.readWeatherFile(weatherfile, starttime=sdt, endtime=sdt, source='SAM')  
                    
                    demo.setGround(albedo) 
                    mymodule = bifacial_radiance.ModuleObj(name='PVmod', x=1, y=2)
                    sceneDict = {'pitch':pitch,'clearance_height':clearance_height, 'nMods': 10, 'nRows': 5, 'azimuth': sazmNS}  
                    demo.set1axis(limit_angle = limit_angle, backtrack = False, gcr=gcr, cumulativesky = cumulativesky,
                                 fixed_tilt_angle=90, azimuth=sazmNS)
                    demo.gendaylit1axis()
                    demo.makeScene1axis(module=mymodule,sceneDict=sceneDict) #makeScene creates a .rad file with 20 modules per row, 7 rows.
                    demo.makeOct1axis()
                    for rr in range (0, len(rowsWanted)):
                        for mm in range(0, len(modsWanted)):
                            writefiletitle = '_NS_'+str(mm).zfill(2)+'-'+str(rr).zfill(2)+'_CH_'+str(clearance_height)+'_rtr_'+str(pitch)+'.csv'
                            demo.analysis1axis(customname=writefiletitle, sensorsy = [9,9], sensorsx = [6,6], 
                                               modWanted = modsWanted[mm], rowWanted = rowsWanted[rr])

                    sceneDict = {'pitch':pitch,'clearance_height':clearance_height, 'nMods': 9, 'nRows': 5, 'azimuth': sazmEW}  
                    demo.set1axis(limit_angle = limit_angle, backtrack = False, gcr=gcr, cumulativesky = cumulativesky,
                                 fixed_tilt_angle=90, azimuth=sazmEW)
                    demo.gendaylit1axis()
                    demo.makeScene1axis(module=mymodule,sceneDict=sceneDict) #makeScene creates a .rad file with 20 modules per row, 7 rows.
                    demo.makeOct1axis()
                    for rr in range (0, len(rowsWanted)):
                        for mm in range(0, len(modsWanted)):
                            writefiletitle = '_EW_'+str(mm).zfill(2)+'-'+str(rr).zfill(2)+'_CH_'+str(clearance_height)+'_rtr_'+str(pitch)+'.csv'
                            demo.analysis1axis(customname=writefiletitle, sensorsy = [9,9], sensorsx = [6,6], 
                                               modWanted = modsWanted[mm], rowWanted = rowsWanted[rr])


# In[ ]:




