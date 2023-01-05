#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
from pathlib import Path
import bifacial_radiance
bifacial_radiance.__version__


# In[2]:


testfolder = testfolder = str(Path().resolve().parent.parent / 'bifacial_radiance' / 'SouthPole')
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[3]:


TMY3Weatherfile = r'C:\Users\sayala\Desktop\SOUTHPOLE\SoutPole_TMY3.csv'


# # Round Setup

# In[4]:


demo = bifacial_radiance.RadianceObj("SouthPole", path = testfolder)  # Create a RadianceObj 'object'
demo.setGround(0.62)
metdata = demo.readWeatherFile(TMY3Weatherfile, coerce_year=2021) 
timestamp = metdata.datetime.index(pd.to_datetime('2021-12-24 13:0:0 -0'))
demo.gendaylit(timestamp) 

# For sanity check, we are creating the same module but with different names for each orientation.
numpanels=1 
ygap = 0.01 # m Spacing between modules on each shed.
y=2   # m. module size, one side
x=1   # m. module size, other side. for landscape, x > y
mymodule = demo.makeModule(name='module',y=y,x=x, numpanels=numpanels, ygap=ygap)


# In[5]:


Rays = 15
pitch = 5
innerR = 5
nMods = 1
nRows = 10
clearance_height = 0.5

sceneObjDict = {}
for rr in range(0, Rays):
    ray_azm = 0 + 360*rr/Rays
    centerpitch = innerR + pitch*(nRows-1)/2         # This might be off by half a pitch, check for even and odd nMods  
    azm = ray_azm - 90  # Radiance and Pvlib use N = 0, so converting
    centerpitch_x = centerpitch*np.cos(np.radians(azm))
    centerpitch_y = centerpitch*np.sin(np.radians(azm))*-1
    sceneDict = {'tilt':90,'pitch':pitch,'clearance_height':clearance_height,'azimuth':ray_azm, 'nMods': 1, 'nRows': nRows, 
             'appendRadfile':True, 'originx': centerpitch_x, 'originy': centerpitch_y} 
    sceneObjDict['sceneObj'+str(rr)] = demo.makeScene(mymodule, sceneDict)  


# In[6]:


octfile = demo.makeOct(demo.getfilelist()) 


# In[7]:


get_ipython().system('rvu -vf views\\front.vp -e .01 -pe 0.3 -vp 0 -27.5 40 -vd 0 0.7071 -0.7071 SouthPole.oct')


# # Square setup

# In[8]:


demo = bifacial_radiance.RadianceObj("SouthPole", path = testfolder)  # Create a RadianceObj 'object'
demo.setGround(0.7)
metdata = demo.readWeatherFile(r'C:\Users\sayala\Desktop\SOUTHPOLE\SoutPole_TMY3.csv', coerce_year=2021) 
timestamp = metdata.datetime.index(pd.to_datetime('2021-12-24 13:0:0 -0'))
demo.gendaylit(timestamp) 

# For sanity check, we are creating the same module but with different names for each orientation.
numpanels=1 
ygap = 0.01 # m Spacing between modules on each shed.
y=2   # m. module size, one side
x=1   # m. module size, other side. for landscape, x > y
xgap = 2
mymodule = demo.makeModule(name='module',y=y,x=x, numpanels=numpanels, xgap=xgap, ygap=ygap)


# In[9]:


nPanels = 2400
print("System Size ", nPanels*.380, "kW")
nMods = 20 # 7         20
nRows = 30 # 11        30
pitch = 4
xgap = 3
z = 0
x = 1
CO = 47          # Center Offset space
goal = 240                   
innerR = xgap+pitch

print("Mega Array Side: ", nMods*z + (nRows-1)*pitch + nMods*x + (nMods-1) * xgap+ CO,  "m")


# In[10]:


Rays = 4
clearance_height = 0.5

sceneObjDict = {}
for rr in range(0, Rays):
    ray_azm = 45 + 360*rr/Rays
    sazm = ray_azm - 45
    centerpitch = innerR + pitch*(nRows-1)/2         # This might be off by half a pitch, check for even and odd nMods  
    azm = ray_azm - 90  # Radiance and Pvlib use N = 0, so converting
    centerpitch_x = centerpitch*np.cos(np.radians(azm))
    centerpitch_y = centerpitch*np.sin(np.radians(azm))*-1
    sceneDict = {'tilt':90,'pitch':pitch,'clearance_height':clearance_height,'azimuth':sazm, 'nMods': nMods, 'nRows': nRows, 
             'appendRadfile':True, 'originx': centerpitch_x, 'originy': centerpitch_y} 
    sceneObjDict['sceneObj'+str(rr)] = demo.makeScene(mymodule, sceneDict)  


# In[11]:


octfile = demo.makeOct(demo.getfilelist()) 


# In[12]:


get_ipython().system('rvu -vf views\\front.vp -e .01 -pe 0.3 -vp 5 -50 50 -vd 0 0.7071 -0.7071 SouthPole.oct')


# In[13]:


demo.genCumSky()
octfile = demo.makeOct(demo.getfilelist()) 


# In[14]:


analysis = bifacial_radiance.AnalysisObj(octfile, demo.basename)  


# In[15]:


# Make a color render and falsecolor image of the scene.
analysis.makeImage('side.vp')
analysis.makeFalseColor('side.vp')


# ### Analysis

# In[16]:


demo.gendaylit(timestamp) 
demo.makeOct()


# In[17]:


sensorsy=4  # 1 per module. consider increasing the number but be careful with sensors in the space between modules.
analysis = bifacial_radiance.AnalysisObj(octfile, demo.basename)  
frontscan, backscan = analysis.moduleAnalysis(sceneObj1, sensorsy=sensorsy)
frontdict, backdict = analysis.analysis(octfile, "EastFacingShed", frontscan, backscan)  # compare the back vs front irradiance  

frontscan, backscan = analysis.moduleAnalysis(sceneObj2, sensorsy=sensorsy )
frontdict2, backdict2 = analysis.analysis(octfile, "WestFacingShed", frontscan, backscan)  # compare the back vs front irradiance  


# ### Analysis LOOP

# In[ ]:


# Run Analysis
for obj in sceneObjDict:
    for mm in range(1, nMods+1):
        for rr in range(1, nRows+1):
            frontscan, backscan = analysis.moduleAnalysis(sceneObjDict[obj], sensorsy=4, sensorsx = 4, modWanted = mm, rowWanted = rr)
            frontdict, backdict = analysis.analysis(octfile, obj, frontscan, backscan)  # compare the back vs front irradiance  


# In[ ]:


# Compile Results
bifaciality = 0.7

#filetitle = 'irr_sceneObj0_Mod_1_Row_3_Row3_Module1.csv'
for obj in sceneObjDict:
    for mm in range(1, nMods+1):
        for rr in range(1, nRows+1):
            filetitle = 'results\irr_'+obj+'_Row'+rr+'_Module'+mm+'.csv'
            data=load.read1Result(filetitle)
            Gpoa = data['Wm2Front'].mean() + data['Wm2Back'].mean()*bifaciality

