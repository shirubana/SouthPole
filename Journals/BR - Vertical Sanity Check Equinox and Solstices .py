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


testfolder = r'TEMP\RADIANCE'
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[3]:


# LOOP
pitchs = [2, 3, 5] 
CHs = [0.3, 0.5, 0.75, 1.0]
albs = [0.22, 0.8]
locs = [722740, 727930 ]
locsnames = ['Tucson', 'Seattle']


# In[4]:


demo = bifacial_radiance.RadianceObj('Sim', path=testfolder)  


# In[5]:


deltastyle = 'SAM'  # 
tilt = 90                   # PV tilt (deg)
sazm = 180                  # PV Azimuth(deg) or tracker axis direction
albedo = 0.80               # ground albedo
clearance_height = 0.5
pitch = 3                   # row to row spacing in normalized panel lengths. 
rowType = "interior"        # RowType(first interior last single)
transFactor = 0.013         # TransmissionFactor(open area fraction)
sensorsy = 12                # sensorsy(# hor rows in panel)   <--> THIS ASSUMES LANDSCAPE ORIENTATION 
PVfrontSurface = "glass"    # PVfrontSurface(glass or ARglass)
PVbackSurface = "glass"     # PVbackSurface(glass or ARglass)

# Calculate PV Output Through Various Methods    
# This variables are advanced and explored in other tutorials.
#calculateBilInterpol = True         # Only works with landscape at the moment.
#calculatePVMismatch = True
#portraitorlandscape='landscape'   # portrait or landscape
#cellsnum = 72
#bififactor = 1.0
#agriPV = True                       # Returns ground irradiance values

# Tracking instructions
tracking=False
backtrack=False
limit_angle = 60

sazmNS = 180                  # PV Azimuth(deg) or tracker axis direction
sazmEW = 90                  # PV Azimuth(deg) or tracker axis direction

cumulativesky = False

startdate = ['03_21', '06_21', '12_21']

for idx in startdate:
    for ii in range(0, len(locs)):
        for jj in range(0, len(albs)):
            for zz in range(0, len(CHs)):
                for ww in range(0, len(pitchs)):

                    loc = locs[ii]
                    locname = locsnames[ii]
                    albedo = albs[jj]
                    clearance_height = CHs[zz]
                    pitch = pitchs[ww]
                    gcr = 2/pitch
                    weatherfile = r'C:\Users\sayala\Desktop\VERTICAL\{}TYA.CSV'.format(loc)
                    writefiletitle = 'NS_'+locname+'_Alb_'+str(albedo)+'_CH_'+str(clearance_height)+'_rtr_'+str(pitch)+'.csv'
                    
                    demo.setGround(albedo) 
                    metdata = demo.readWeatherFile(weatherfile, starttime=idx, endtime=idx)  
                    mymodule = bifacial_radiance.ModuleObj(name='PVmodw', x=1, y=2)
                    sceneDict = {'pitch':pitch,'hub_height':clearance_height, 'nMods': 20, 'nRows': 7, 'azimuth': sazmNS}  
                    demo.set1axis(limit_angle = limit_angle, backtrack = backtrack, gcr=gcr, cumulativesky = cumulativesky,
                                 fixed_tilt_angle=90, azimuth=sazmNS)
                    demo.gendaylit1axis()
                    demo.makeScene1axis(module=mymodule,sceneDict=sceneDict) #makeScene creates a .rad file with 20 modules per row, 7 rows.
                    demo.makeOct1axis()
                    demo.analysis1axis(customname=writefiletitle)
                    
                    
                    writefiletitle = 'EW_'+locname+'_Alb_'+str(albedo)+'_CH_'+str(clearance_height)+'_rtr_'+str(pitch)+'.csv'

                    sceneDict = {'pitch':pitch,'hub_height':clearance_height, 'nMods': 20, 'nRows': 7, 'azimuth': sazmEW} 
                    demo.set1axis(limit_angle = limit_angle, backtrack = backtrack, gcr=gcr, cumulativesky = cumulativesky,
                                 fixed_tilt_angle=90, azimuth=sazmEW)
                    demo.gendaylit1axis()
                    demo.makeScene1axis(module=mymodule,sceneDict=sceneDict) #makeScene creates a .rad file with 20 modules per row, 7 rows.
                    demo.makeOct1axis()
                    demo.analysis1axis(customname=writefiletitle)

