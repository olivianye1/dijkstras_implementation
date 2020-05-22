"""
Olivia Nye
Project 2 - Final Submission (Parts 1-3)

Implements Dijkstras algorithm using a min-heap to read in data from distance graph files,
format the data into a graph in the form of an adjacency list, find the shortest path from a source
location to a target location, and outputs the path and its distance to a .txt file

*Extra credit is in a separate file
"""
import math

infinity = float(math.inf)

#node in heap
class Element:
    def __init__(self, vId, totDist):
        self.vId = vId
        self.totDist = totDist
        self.prev = None

#priority queue (minheap) itself
class MinHeap:
    def __init__(self):
        self.q = []

#node in graph
class Edge:
    def __init__(self, vF, vT, w):
        self.vFrom = vF
        self.vTo = vT
        self.weight = w


# vid of element at current index in the heap : totalDist it takes to get to that element in the shortest path
vid_dist_dict = {}

# vid of element at current index in the heap : vid of the element that, in the shortest path, precedes the element at the current index in the heap
vid_prev_dict = {}

# vid of element at current index in the heap : index in the heap
vid_index_dict = {}

# (Edge.vFrom (prev), Edge.vTo(current) : Edge.weight
edge_weight_dict = {}

#creates an adjacency list data structure from an input .gr file
def create_graph(filePath):
    file = open(filePath, "r")

    adjacencyList = {}

    lines = file.readlines()
    for line in lines:
        l = str(line)
        split_line = l.split()

        if split_line[0] == "a":
            vFrom = split_line[1]
            vTo = split_line[2]
            weight = int(split_line[3])

            # if vFrom is already a key in the adjacencyList
            if vFrom in adjacencyList:
                edgelist = adjacencyList.get(vFrom)
                edgelist.append(Edge(vFrom, vTo, weight))
                adjacencyList[vFrom] = edgelist
                # for edge in edgelist:
                #     if edge.vTo not in adjacencyList:
                #         adjacencyList[edge.vTo] = []
            else:
                edgelist = [Edge(vFrom, vTo, weight)]
                adjacencyList[vFrom] = edgelist
                #for edge in edgelist:
                    #make sure nodes that don't point to anything end up in the graph
                    # if edge.vTo not in adjacencyList:
                    #     adjacencyList[edge.vTo] = []
    # saves weight of the edges to dictionary, for ease of calculating path weight later
    for key in adjacencyList:
        for edge in adjacencyList.get(key):
            edge_weight_dict[(edge.vFrom, edge.vTo)] = edge.weight
    return adjacencyList

#formats and prints the adjacency list as a string to visualize the graph
def toString(graph):
    for key in graph:
        #get key
        for edge in graph.get(key):
            vfrom = edge.vFrom
            vto = edge.vTo
            vw = edge.weight

            string = key + ": vFrom = " + vfrom + ", vTo = " + vto + ", weight = " + str(vw)
            print(string)
        if graph.get(key) == []:
            string = key + ": none"
            print(string)


#decrease_key
def update_tot_dist(myHeap, vertexId, newTotDist, newPrev):

    currElementIndex = vid_index_dict[vertexId]
    myHeap.q[currElementIndex].totDist = newTotDist
    myHeap.q[currElementIndex].prev = newPrev.vId

    update_dicts(myHeap, currElementIndex)

    return min_heapify(myHeap, currElementIndex)


#inserts new element to the bottom of the heap
def add_element(myHeap, vertexId):
    newElement = Element(vertexId, infinity)
    myHeap.q.append(newElement)
    update_dicts(myHeap, len(myHeap.q)-1)
    return myHeap


#corrects all of the dictionaries to hold accurate info
def update_dicts(myHeap, index):
    vid_dist_dict[myHeap.q[index].vId] = myHeap.q[index].totDist
    vid_prev_dict[myHeap.q[index].vId] = str(myHeap.q[index].prev)
    vid_index_dict[myHeap.q[index].vId] = index

#swaps the positions of 2 elements in the min heap
def swap(myHeap, index1, index2):
    #save as temp values
    temp1 = myHeap.q[index1]
    temp2 = myHeap.q[index2]

    #perform the swap
    myHeap.q[index1] = temp2
    myHeap.q[index2] = temp1

    #corrrect dictionaries
    update_dicts(myHeap, index1)
    update_dicts(myHeap, index2)

    return myHeap

#removes the minimum element from the priority queue
def extract_min(myHeap):
    #swap minimum and maximum elements in myHeap.q
    myHeap = swap(myHeap, 0, -1)
    del myHeap.q[-1]
    myHeap = min_heapify(myHeap, 0)
    return myHeap

#helper function for min_heapify - calculates position of an element's left child in the array representing a heap
def get_left_child_index(index):
    leftInd = (2*(index + 1)) - 1
    return leftInd

#helper function for min_heapify - calculates position of an element's right child in the array representing a heap
def get_right_child_index(index):
    rightInd = (2*(index + 1))
    return rightInd

#helper function for min_heapify - calculates position of an element's parent in the array representing a heap
def get_parent_index(index):
    return math.floor(index/2)


#implements the priority queue part of the algorithm as a min-heap
def min_heapify(myHeap, index):
    leftI = get_left_child_index(index)
    rightI = get_right_child_index(index)
    smallest = index

    # if q is empty or index is not in the heap
    if len(myHeap.q) <= 1 or index > len(myHeap.q)-1:
        return myHeap
    # if index is a leaf (doesn't have kids)
    if (leftI > len(myHeap.q))-1 and (rightI > len(myHeap.q))-1:
        # if index is not the root
        if index != 0:
            # make sure it's bigger than its parent
            if myHeap.q[get_parent_index(index)].totDist < myHeap.q[index].totDist:
                myHeap = swap(myHeap, get_parent_index(index), index)
                myHeap = min_heapify(myHeap, get_parent_index(index))
            else:
                return myHeap

    #check parent
    if index != 0:
        # make sure it's bigger than its parent
        if myHeap.q[get_parent_index(index)].totDist < myHeap.q[index].totDist:
            myHeap = swap(myHeap, get_parent_index(index), index)
            myHeap = min_heapify(myHeap, get_parent_index(index))

    #check children
    # if left exists and is smaller than value of index
    if leftI <= len(myHeap.q)-1 and myHeap.q[leftI].totDist < myHeap.q[smallest].totDist:
        smallest = leftI
    # if right exists and is smaller than value of index
    if rightI <= len(myHeap.q)-1 and myHeap.q[rightI].totDist < myHeap.q[smallest].totDist:
        smallest = rightI

    if smallest != index:
        myHeap = swap(myHeap, smallest, index)
        myHeap = min_heapify(myHeap, smallest+1)
    return myHeap


# traces the shortest path, formats the path into a formatted string, and writes the path weight and path description to an output file
def shortest(vid, sourceVid, pathway, graph, shortestDist, targetFile):
    #traces path from target node down to source node
    prevVid = vid_prev_dict[vid]
    if prevVid != sourceVid:
        pathway.append(prevVid)
        shortestDist += edge_weight_dict[(prevVid, vid)]
        #print(pathway)
        shortest(prevVid, sourceVid, pathway, graph, shortestDist, targetFile)
    #once you've reached the source node, don't need to trace any further
    if prevVid == sourceVid:
        pathway.append(prevVid)
        shortestDist += edge_weight_dict[(prevVid, vid)]

        #formulate the path into a string that will be outputted to the file
        pathDescription = str(shortestDist)
        pathDescription += "\n"
        while len(pathway) != 0:
            #the pathway is currently backwards, so we pop (remove last element) to make it forward (source to target in the description)
            curr = pathway.pop()
            pathDescription += curr
            pathDescription += "\n"
        # write to file
        file = open(targetFile, "w")
        file.write(pathDescription)
        file.close()


#specify source by user, turn it into 0 by finding it's position and updateing tot dist on it
def FindShortestPath(inputFile, sourceKey, targetKey, targetFile):
    graph = create_graph(inputFile)
    myHeap = MinHeap()

    validTarget = False
    validSource = False

    for key in graph:
        if key == sourceKey:
            validSource = True
            #prepend to make sourceKey the min value in the heap
            newElement = Element(sourceKey, 0)
            myHeap.q.insert(0, newElement)
            update_dicts(myHeap, 0)
            #account for how prepending source increments index of all other elements in the heap by 1
            i = 0
            while i < len(myHeap.q) - 1:
                i += 1
                vid_index_dict[myHeap.q[i].vId] = i
        else:
            if key == targetKey:
                validTarget = True
            myHeap = add_element(myHeap, key)
    if (validTarget is False) or (validSource is False):
        print("INVALID REQUEST: Requested invalid target key and/or source key!")
        return

    while len(myHeap.q) != 0:
        current = myHeap.q[0]

        if len(graph.get(current.vId)) == 0:
            myHeap = extract_min(myHeap)
            break
        for neighbor in graph.get(current.vId):
            neighborIndex = vid_index_dict[neighbor.vTo]
            neighborElement = myHeap.q[neighborIndex]

            #all paths will be less than infinity, so always update if it's tot dist hasn't been updated yet
            if neighborElement.totDist == infinity:
                # adding current.totDist to infinity would just make a bigger infinity so we pretend neighborElement.totDist is 0 when we update
                myHeap = update_tot_dist(myHeap, neighborElement.vId, current.totDist, current)
            #if this creates a shorter path to this node than the current path to it, update
            elif (current.totDist + neighbor.weight) < neighborElement.totDist:
                myHeap = update_tot_dist(myHeap, neighborElement.vId, current.totDist + neighbor.weight, current)
        myHeap = extract_min(myHeap)
    #add target key to the path
    pathway = [targetKey]
    shortestDist = 0
    #trace the path from the target back to the source
    shortest(targetKey, sourceKey, pathway, graph, int(shortestDist), targetFile)
    print("Done")


#FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "1", "1276", "NY_shortest_path_1_1276.txt")
#FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "1", "2", "NY_shortest_path_1_2.txt")
#FindShortestPath("/Users/olivianye/PycharmProjects/Project2/USA-road-d.NY.gr", "9", "592", "NY_shortest_path_9_592.txt")









