Algorithms Project 2 by Olivia Nye 


Dijkstras_OliviaNye.py --> final submission (parts 1-3) 
	Description: 
		Implements Dijkstras algorithm using a min-heap to read in data from distance graph files,
		format the data into a graph in the form of an adjacency list, find the shortest path from a source
		location to a target location, and outputs the path and its distance to a .txt file.
	Instructions:
		1. Save file and load file in any python IDE (PyCharm, Idle, etc) or CD into the file's location in a terminal
		2. Ensure that the USA-road-d.NY.gr file is downloaded, note the path of it
		3. Uncomment one of the three commands in lines 288-290 and change the first parameter to the path to the 
		   USA-road-d.NY.gr file on your machine. 
		   These commands are listed below:
				3a. The example path from the assignment -- from 1 to 1276: 
					FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "1", "1276", "NY_shortest_path_1_1276.txt")
				3b. Additional Tester path from 1 to 2				
					FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "1", "2", "NY_shortest_path_1_2.txt")
				3c. Additional Tester path from 9 to 592
					FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "9", "592", "NY_shortest_path_9_592.txt")

USA-road-d.NY.gr
	Description:
		Sample input file for Dijkstras_OliviaNye.py. New York distance graph data from
		http://users.diag.uniroma1.it/challenge9/download.shtml
		
NY_shortest_path_1_1276.txt	
	Description:
		Sample output file from Dijkstras_OliviaNye.py for the example path from the assignment (1 to 1276) (3a).
		Also the sample input file (saved to pathfile variable in the program) for Map_OliviaNye.py. 
	Contents:
		6529
		1
		1363
		1358
		1357
		1356
		1276

NY_shortest_path_1_2.txt
	Description:
		Sample output file for additional tester path from 1 to 2 (3b)
	Content: 
		803
		1
		2

NY_shortest_path__9_592.txt
	Description:
		Sample output file for additional tester path from 9 to 592 (3c)
	Contents:
		4170
		9
		603
		594
		588
		592
		
		
Map_OliviaNye.py
	Description: 
		Extra credit option #2. Reads in an output file from Dijkstras_OliviaNye.py (the example one from the 
		assignment description "NY_shortest_path_1_1276.txt" is hard coded in the file for ease of 
		running/testing for grading) and a coordinates file, and plots the path on a map using Google Maps 
		API and the GMAPS library. 
	NOTE:
		THIS PROGRAM RUNS EXCLUSIVELY IN JUPYTER NOTEBOOK. This has been approved by Prof. Maus. 
	Instructions:
		1. If you do not already have it installed, helpful instructions can be found 
		   here: https://jupyter.org/install.
		2. Navigate to a terminal and run the following commands:
			$ conda install -c conda-forge gmaps
			$ jupyter nbextension enable --py --sys-prefix widgetsnbextension
			$ pip install gmaps
			$ jupyter nbextension enable --py --sys-prefix gmaps
			$ conda install nbconvert
			(Note: if you have trouble, reference this page https://jupyter-gmaps.readthedocs.io/en/latest/install.html)
		3. Launch Jupyter Notebook 
		4. Upload Map_OliviaNye.py to Jupyter Notebook OR click "New" --> "Python 3" and copy-paste the 
		   following code into the new notebook: 
				```
				pip install gmaps 
		
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
				```
		5. Change the file path for coordfile to wherever you have "USA-road-d.NY.co" saved. Note that
		   I provided this file with my submission.
		6. Change the file path for pathfile to wherever you have "NY_shortest_path_1_1276.txt" saved. 
		   Note that I provided this file with my submission.
		7. Click Run
		8. (Sometimes). You may have to restart the kernel and re-runafter running ```pip install gmaps``` 
		   for the first time in order for the graph to generate.
		   
USA-road-d.NY.co
	Description:
		Sample input coordinates file (saved to coordfile variable in the program) for Map_OliviaNye.py. New York 
		coordinates data from http://users.diag.uniroma1.it/challenge9/download.shtml
		
map_output.png
	Description:
		Screenshot of the results of running Map_OliviaNye.py
		
README.txt
	Description:
		This file. Describes submission files and running instructions. 		














		