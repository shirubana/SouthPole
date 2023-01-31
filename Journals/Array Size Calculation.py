#!/usr/bin/env python
# coding: utf-8

# # Array Size Calculation

# In[1]:


import numpy as np


# In[2]:


SystemCapacity = 354 #kW, for solar
panel_nameplate = .380 # kW
nSections = 4

# Module Sizes
# Portrait mode, typically x = 1 and y =2 for this. For landscape, rotate numbers.
x = 1 # Module size parallel to ground
y = 2 # Module edge in the Z direction. 

pitch = 8 # a.k.a. row-to-row distance
xgap = 1 # module-to-module space along the row axis. 
         # This account for the sleds, racking, as well as increase diffuse light in the array/minimize shading.


# In[3]:


nPanels = np.round(SystemCapacity/panel_nameplate/nSections)*nSections  # 4 sections (NSEW), that's why dividing and rounding so it is a number dividable by 4. 
sectionnPanels = nPanels/nSections

print("Panels in Field", int(nPanels))
print("Panels per section ", int(sectionnPanels))


# In[4]:


squareness = int(pitch/(x+xgap))
print("nMods has to be ~", squareness, "x nRows for 'squareness'")


# In[5]:


nMods = int(np.ceil(sectionnPanels/squareness/2))
nRows = int(np.ceil(sectionnPanels/nMods))
print("nMods", nMods, "nRows", nRows)


# In[6]:


sectionnPanelsCorrected = nMods*nRows # Correcting for rounding
nPanelsCorrected = sectionnPanelsCorrected*4
SystemCapacityCorrected = nPanelsCorrected*panel_nameplate
 
print("Corrected numbers: \n\t", sectionnPanelsCorrected, " per Section\n",
      "\t", nPanelsCorrected, "for the whole System\n",
      "\t", SystemCapacityCorrected, " kW System Capcaity")


# In[7]:


CO = 20          # Section Offset space. giving enough space for cars to go through, inverter systems etc.

print("Section Size: ", nMods + (nMods-1) * xgap , " x ", (nRows-1)*pitch, " m ")
print("Mega Array Side: ", nMods + (nMods-1) * xgap + CO + (nRows-1)*pitch,  "m")


# # Considering racking bays of 5-7 modules

# In[8]:


modulesInBay = 6
baygap = 2 # m


# In[9]:


nBays = int(np.ceil(nMods/6))
nModsBayCorrected = nBays*modulesInBay

sectionnPanelsBayCorrected = int(nModsBayCorrected*nRows) # Correcting for rounding
nPanelsBayCorrected = int(sectionnPanelsBayCorrected*4)
SystemCapacityBayCorrected = nPanelsBayCorrected*panel_nameplate
 
print("Corrected numbers: \n\t", sectionnPanelsBayCorrected, " modules per Section\n",
      "\t", nBays, " bays of ", nModsBayCorrected, " modules each in the row,", nRows, " rows \n",
      "\t", nPanelsBayCorrected, "for the whole System\n",
      "\t", SystemCapacityBayCorrected, " kW System Capcaity")


# In[10]:


print("Section Size per Side: ", nMods + ((nMods/modulesInBay) - 1) * baygap , " x ", (nRows-1)*pitch, " m ")
print("Mega Array Side: ", nMods + ((nMods/modulesInBay) - 1) * baygap + CO + (nRows-1)*pitch,  "m")


# ## Imaging

# In[ ]:


import pandas as pd
import os
from pathlib import Path
import bifacial_radiance
bifacial_radiance.__version__

testfolder = r'TEMP\SquareDesign'
if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[ ]:


rawfile = r'..\..\IOFiles\SouthPole_2021_WeatherFile.csv'
demo = bifacial_radiance.RadianceObj("SouthPole", path = testfolder)  # Create a RadianceObj 'object'
demo.setGround(0.7)
metdata = demo.readWeatherFile(rawfile, source='SAM') 


# In[ ]:


# For sanity check, we are creating the same module but with different names for each orientation.
mymodule = demo.makeModule(name='module',y=y,x=x, xgap=xgap)


# In[ ]:


timestamp = metdata.datetime.index(pd.to_datetime('2021-12-24 13:0:0 -0'))
demo.gendaylit(timestamp) 


# In[ ]:


clearance_height = 0.5

sceneObjDict = {}
for rr in range(0, nSections):
    ray_azm = 45 + 360*rr/nSections
    sazm = ray_azm - 45
    centerpitch = CO + pitch*(nRows-1)/2         # This might be off by half a pitch, check for even and odd nMods  
    azm = ray_azm - 90  # Radiance and Pvlib use N = 0, so converting
    centerpitch_x = centerpitch*np.cos(np.radians(azm))
    centerpitch_y = centerpitch*np.sin(np.radians(azm))*-1
    sceneDict = {'tilt':90,'pitch':pitch,'clearance_height':clearance_height,'azimuth':sazm, 'nMods': nMods, 'nRows': nRows, 
             'appendRadfile':True, 'originx': centerpitch_x, 'originy': centerpitch_y} 
    sceneObjDict['sceneObj'+str(rr)] = demo.makeScene(mymodule, sceneDict)  


# In[ ]:


octfile = demo.makeOct() 


# In[ ]:


get_ipython().system('rvu -vf views\\front.vp -e .01 -pe 0.3 -vp 5 -50 50 -vd 0 0.7071 -0.7071 SouthPole.oct')


# ![image.png](attachment:image.png)