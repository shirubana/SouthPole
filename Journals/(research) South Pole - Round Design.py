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


testfolder = r'TEMP\RoundDesign'
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[3]:


rawfile = r'..\..\SAM_SP_WeatherFile.csv'
demo = bifacial_radiance.RadianceObj("SouthPole", path = testfolder)  # Create a RadianceObj 'object'
demo.setGround(0.7)
metdata = demo.readWeatherFile(rawfile, source='SAM') 


# In[4]:


timestamp = metdata.datetime.index(pd.to_datetime('2021-12-24 13:0:0 -0'))
demo.gendaylit(timestamp) 

# For sanity check, we are creating the same module but with different names for each orientation.
numpanels=1 
ygap = 0.01 # m Spacing between modules on each shed.
y=2   # m. module size, one side
x=1   # m. module size, other side. for landscape, x > y
xgap = 2
mymodule = demo.makeModule(name='module',y=y,x=x, numpanels=numpanels, xgap=xgap, ygap=ygap)


# In[ ]:


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


# In[ ]:


octfile = demo.makeOct(demo.getfilelist()) 


# In[ ]:


get_ipython().system('rvu -vf views\\front.vp -e .01 -pe 0.3 -vp 0 -27.5 40 -vd 0 0.7071 -0.7071 SouthPole.oct')


# In[ ]:


demo.genCumSky()
octfile = demo.makeOct(demo.getfilelist()) 


# In[ ]:


# Make a color render and falsecolor image of the scene.
analysis.makeImage('side.vp')
analysis.makeFalseColor('side.vp')


# In[ ]:


for obj in sceneObjDict:
    for mm in range(1, nMods+1):
        for rr in range(1, nRows+1):
            frontscan, backscan = analysis.moduleAnalysis(sceneObjDict[obj], sensorsy=4, sensorsx = 4, modWanted = mm, rowWanted = rr)
            frontdict, backdict = analysis.analysis(octfile, obj, frontscan, backscan)  # compare the back vs front irradiance  


# In[ ]:


bifaciality = 0.7

filetitle = 'irr_sceneObj0_Mod_1_Row_3_Row3_Module1.csv'
for obj in sceneObjDict:
    for mm in range(1, nMods+1):
        for rr in range(1, nRows+1):
            filetitle = 'results\irr_'+obj+'_Row'+rr+'_Module'+mm+'.csv'
            data=load.read1Result(filetitle)
            Gpoa = data['Wm2Front'].mean() + data['Wm2Back'].mean()*bifaciality


# In[ ]:


sensorsy=4  # 1 per module. consider increasing the number but be careful with sensors in the space between modules.
analysis = bifacial_radiance.AnalysisObj(octfile, demo.basename)  
frontscan, backscan = analysis.moduleAnalysis(sceneObj1, sensorsy=sensorsy)
frontdict, backdict = analysis.analysis(octfile, "EastFacingShed", frontscan, backscan)  # compare the back vs front irradiance  

frontscan, backscan = analysis.moduleAnalysis(sceneObj2, sensorsy=sensorsy )
frontdict2, backdict2 = analysis.analysis(octfile, "WestFacingShed", frontscan, backscan)  # compare the back vs front irradiance  

