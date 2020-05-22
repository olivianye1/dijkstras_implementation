#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install gmaps


# In[23]:



import gmaps.datasets


#read in coordinates file
coordfile = open("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.co", "r")
cDict = {}
lines = coordfile.readlines()
for line in lines:
    l = str(line)
    split_line = l.split()
    if split_line[0] == "v":
        vId = split_line[1]
        #only 2 significant digits
        lat = int(split_line[2]) / 1000000
        long = int(split_line[3]) / 1000000
        #map vertexIds to their coordinates
        coords = (long, lat)
        cDict[vId] = coords
        
#read in output file from other program        
pathfile = open("/Users/olivianye/PycharmProjects/Project2/NY_shortest_path_1_1276.txt", "r")
lines = pathfile.read().splitlines()
#remove line that states distance of path (first line)
lines.pop(0)
#new first line is our source
startPointId = lines[0]
startPointCoords = tuple(cDict[startPointId])
#last line is our target
endPointId = lines[-1]
endPointCoords = tuple(cDict[endPointId])
lines.pop(0)
lines.pop(-1)

stopCoords = []
#rest of our lines are stops or "waypoints"
for line in lines:
    stopId = line
    stopCoord = tuple(cDict[stopId])
    stopCoords.append(stopCoord)
    

#hook up to my google maps API key
gmaps.configure(api_key="AIzaSyD3_zabz-wq9GhxEXy4YC1aZW7cAZCc2vQ")

#create a base map
fig = gmaps.figure()
# map points and path
fig.add_layer(gmaps.directions_layer(startPointCoords, endPointCoords, waypoints=stopCoords, travel_mode='BICYCLING'
                                     ,show_markers=True,stroke_color='red', stroke_weight=8.0, stroke_opacity=1.0))
#display map
fig


# In[ ]:





# In[ ]:





# In[ ]:




