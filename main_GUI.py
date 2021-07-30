import heapq
import math
import Prims_And_Kruskals
import tkinter

main = tkinter.Tk()
main.title("Graphs Visualization")
main.resizable(False, False)

width, height = 960, 720

canvas = tkinter.Canvas(main, width=width, height=height)
canvas.grid(row=3, column=0, columnspan=3)

# node clicked to add arc
nodeClicked = False
nodeName = ""
invsNodeDict = {}

# list of pending after methods
afterList = []

# dict of (coords, radius)
coordDict = {}

# variables for Prims
nodeDict = {}

# variables for Kruskals

# dict of edges to remove and edit
canvasEdgesDict = {}

mst = []

count = 0

nodeCounter = 1

# kruskals

# get new value for adding arc


def getValue(nodeName, secondNodeName):
    popup = tkinter.Toplevel(main)

    popup.title("Enter value of edge")

    popup.resizable(False, False)

    label = tkinter.Label(popup, text="Enter a value for the selected edge:")
    label.grid(row=0, column=0)

    entry = tkinter.Entry(popup, width=50)
    entry.grid(row=0, column=1)
    entry.insert(0, "1")

    button = tkinter.Button(popup, text="Confirm", command=lambda:  add_arc_with_value(
        int(entry.get()), nodeName, secondNodeName, popup))
    button.grid(row=1, column=0, columnspan=2)


# one pass of heappush
def heappush_prims(counter, limit, edgeList, priorityQueue, viewTime, visited):
    if counter < limit:

        edge = edgeList[counter]

        if not (edge[1] in visited and edge[2] in visited):
            heapq.heappush(priorityQueue, edge)
            if (edge[1], edge[2]) in canvasEdgesDict:
                arc, text, isArc = canvasEdgesDict[(edge[1], edge[2])]
                if isArc:
                    if canvas.itemcget(arc, "outline") == "purple1":
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, outline="purple1"))
                        afterList.append(changedArc)
                    else:
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, outline="white"))
                        afterList.append(changedArc)
                    canvas.itemconfig(arc, outline="gold")
                else:
                    if canvas.itemcget(arc, "fill") == "purple1":
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, fill="purple1"))
                        afterList.append(changedArc)
                    else:
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, fill="white"))
                        afterList.append(changedArc)
                    canvas.itemconfig(arc, fill="gold")
            elif (edge[2], edge[1]) in canvasEdgesDict:
                arc, text, isArc = canvasEdgesDict[(edge[2], edge[1])]

                if isArc:
                    if canvas.itemcget(arc, "outline") == "purple1":
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, outline="purple1"))
                        afterList.append(changedArc)
                    else:
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, outline="white"))
                        afterList.append(changedArc)
                    canvas.itemconfig(arc, outline="gold")

                else:
                    if canvas.itemcget(arc, "fill") == "purple1":
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, fill="purple1"))
                        afterList.append(changedArc)
                    else:
                        changedArc = main.after(viewTime,
                                                lambda: canvas.itemconfig(arc, fill="white"))
                        afterList.append(changedArc)
                    canvas.itemconfig(arc, fill="gold")

            heapPushPrims = main.after(viewTime, lambda: heappush_prims(
                counter + 1, limit, edgeList, priorityQueue, viewTime, visited))
            afterList.append(heapPushPrims)

        else:
            heappush_prims(
                counter + 1, limit, edgeList, priorityQueue, viewTime, visited)

# implementation of prims


def one_turn_prims(graph, visited, priorityQueue, viewTime):
    leastNum = heapq.heappop(priorityQueue)
    numEdges = 0

    # color lowest edge - current edge being processed
    if (leastNum[1], leastNum[2]) in canvasEdgesDict:
        arc, text, isArc = canvasEdgesDict[(leastNum[1], leastNum[2])]
        if isArc:
            previousColor = canvas.itemcget(arc, "outline")
            canvas.itemconfig(arc, outline="firebrick3")
        else:
            previousColor = canvas.itemcget(arc, "fill")
            canvas.itemconfig(arc, fill="firebrick3")
    elif (leastNum[2], leastNum[1]) in canvasEdgesDict:
        arc, text, isArc = canvasEdgesDict[(leastNum[2], leastNum[1])]
        if isArc:
            canvas.itemconfig(arc, outline="firebrick3")
            previousColor = canvas.itemcget(arc, "outline")
        else:
            canvas.itemconfig(arc, fill="firebrick3")
            previousColor = canvas.itemcget(arc, "fill")

    if leastNum[1] not in visited:
        # color edge that is part of dst
        if isArc:
            canvas.itemconfig(arc, outline="purple1")
        else:
            canvas.itemconfig(arc, fill="purple1")

        previousColor = "purple1"

        mst.append(leastNum)

        nodeCircle, nodeText = nodeDict[leastNum[1]]
        canvas.itemconfig(nodeCircle, outline="RoyalBlue1")

        for edge in graph[leastNum[1]]:
            if not (edge[1] in visited and edge[2] in visited):
                numEdges += 1

        heapPushPrims = main.after(viewTime,
                                   lambda: heappush_prims(0, len(graph[leastNum[1]]), graph[leastNum[1]], priorityQueue, viewTime, visited))
        changeColor = main.after(viewTime * (numEdges + 1),
                                 lambda: canvas.itemconfig(nodeCircle, outline="white"))

        afterList.append(heapPushPrims)
        afterList.append(changeColor)

        visited.add(leastNum[1])

    if priorityQueue:
        if isArc:
            revertColor = main.after(
                viewTime * (numEdges + 1), lambda: canvas.itemconfig(arc, outline=previousColor))
        else:
            revertColor = main.after(
                viewTime * (numEdges + 1), lambda: canvas.itemconfig(arc, fill=previousColor))

        nextTurn = main.after(viewTime * (numEdges + 1), lambda: one_turn_prims(
            graph, visited, priorityQueue, viewTime))

        afterList.append(nextTurn)
        afterList.append(revertColor)


# prims
def prims(graph, viewTime):
    visited = set()

    mst = []

    priorityQueue = []

    initialNode = next(iter(graph))

    visited.add(initialNode)

    # turn initial node blue
    nodeCircle, nodeText = nodeDict[initialNode]

    canvas.itemconfig(nodeCircle, outline="RoyalBlue1")

    numEdges = len(graph[initialNode])

    heappush_prims(0, numEdges, graph[initialNode],
                   priorityQueue, viewTime, visited)

    starting = main.after(viewTime * (numEdges + 1),
                          lambda: one_turn_prims(graph, visited, priorityQueue, viewTime))

    recolorNode = main.after(viewTime * (numEdges),
                             lambda: canvas.itemconfig(nodeCircle, outline="white"))

    afterList.append(starting)


# one pass of kruskal algo
def one_turn_kruskal(dsu, sortedGraph, viewTime):
    global count
    edge = sortedGraph[count]

    length, first, second = edge

    if (edge[1], edge[2]) in canvasEdgesDict:
        arc, text, isArc = canvasEdgesDict[(edge[1], edge[2])]
    elif (edge[2], edge[1]) in canvasEdgesDict:
        arc, text, isArc = canvasEdgesDict[(edge[2], edge[1])]
    else:
        print(canvasEdgesDict, edge, sortedGraph)

    if isArc:
        canvas.itemconfig(arc, outline="gold")
    else:
        canvas.itemconfig(arc, fill="gold")

    if dsu[first] != dsu[second]:
        idToChange = dsu[second]
        idToBe = dsu[first]
        for key in dsu:
            if dsu[key] == idToChange:
                dsu[key] = idToBe
        mst.append(edge)
        if isArc:
            returnCanvas = main.after(viewTime,
                                      lambda: canvas.itemconfig(arc, outline="purple1"))
        else:
            returnCanvas = main.after(viewTime,
                                      lambda: canvas.itemconfig(arc, fill="purple1"))
    else:
        if isArc:
            returnCanvas = main.after(viewTime,
                                      lambda: canvas.itemconfig(arc, outline="white"))
        else:
            returnCanvas = main.after(viewTime,
                                      lambda: canvas.itemconfig(arc, fill="white"))

        afterList.append(returnCanvas)

    count += 1


def kruskal(graph, viewTime):

    sortedGraph = []

    # list of edges

    usedEdges = set()

    for key in graph:
        for edge in graph[key]:
            if (edge[1], key) not in usedEdges and (key, edge[1]) not in usedEdges:
                usedEdges.add((edge[1], edge[2]))
                sortedGraph.append(edge)

    sortedGraph.sort(key=lambda x: x[0])

    # dict of "ids" too quickly find if cycle - quick find algorithm
    dsu = {}
    counter = 0
    for key in graph:
        dsu[key] = counter
        counter += 1

    # iterate through sorted graph
    counter = 0
    for edge in sortedGraph:

        moveCanvas = main.after(viewTime * counter,
                                lambda: one_turn_kruskal(dsu, sortedGraph, viewTime))

        afterList.append(moveCanvas)

        counter += 1

# return list of edges from Adjacency list


def edge_list(graph):

    edgeList = []

    usedEdges = set()

    for key in graph:
        for edge in graph[key]:
            if (edge[1], key) not in usedEdges and (key, edge[1]) not in usedEdges:
                usedEdges.add((edge[1], edge[2]))
                edgeList.append(edge)

    return edgeList

# remove node


def remove_node(event):

    # stop all next events
    clear_canvas()

    canvas_item_id = event.widget.find_withtag('current')[0]

    nodeName = invsNodeDict[canvas_item_id]

    del invsNodeDict[canvas_item_id]

    canvas.delete(canvas_item_id)

    nodeCircle, tempText = nodeDict[nodeName]

    canvas.delete(nodeCircle)
    canvas.delete(tempText)

    del tempGraphFixed[nodeName]

    for key in tempGraphFixed:
        for edgeNum in range(len(tempGraphFixed[key]) - 1, -1, -1):
            if nodeName in tempGraphFixed[key][edgeNum]:
                del tempGraphFixed[key][edgeNum]

    for key in list(canvasEdgesDict.keys()):
        if nodeName in key:
            arc, text, isArc = canvasEdgesDict[key]

            canvas.delete(arc)
            canvas.delete(text)

            del canvasEdgesDict[key]


def add_node(event):
    global nodeCounter

    canvas_item_id = event.widget.find_withtag('current')[0]
    x1, y1, x2, y2 = canvas.coords(canvas_item_id)

    widthCoord = (x1 + x2)/2
    heightCoord = (y1 + y2)/2

    tempText = canvas.create_text(
        widthCoord, heightCoord, font="Times 20", text=str(nodeCounter))

    radius = max(canvas.bbox(tempText)[
        2] - canvas.bbox(tempText)[0], canvas.bbox(tempText)[3] - canvas.bbox(tempText)[1]) / 2 + 10

    nodeCircle = canvas.create_oval(widthCoord - radius, heightCoord - radius,
                                    widthCoord + radius, heightCoord + radius, fill="black")

    canvas.tag_raise(tempText)

    # create invis node for hit detection
    x0, y0, x1, y1 = canvas.coords(nodeCircle)
    invsCircle = canvas.create_oval(
        canvas.coords(nodeCircle), fill="", outline="", tag="node")
    invsNodeDict[invsCircle] = str(nodeCounter)
    canvas.tag_bind(invsCircle, "<Button-1>",
                    node_clicked)

    canvas.tag_bind(invsCircle, "<Button-2>",
                    remove_node)

    # for circle manip later
    nodeDict[str(nodeCounter)] = (nodeCircle, tempText)

    # get coords
    coordDict[str(nodeCounter)] = (widthCoord, heightCoord, radius)

    # add to graph
    tempGraphFixed[str(nodeCounter)] = []

    nodeCounter += 1

# register click to enable arc creation


def node_clicked(event):
    global nodeClicked
    global nodeName
    nodeId = event.widget.find_withtag('current')[0]
    nodeClicked = True
    nodeName = invsNodeDict[nodeId]

# create the outline of the graph in tkinter


def create_basic_graph(graph):

    widthDiv, heightDiv = 13, 9

    cellWidth, cellHeight = width / widthDiv, height / heightDiv

    # radius = min(width/(2 * widthDiv), height/(2 * heightDiv)) - 40

    numNodes = len(graph)

    n = 0

    for heightNum in range(heightDiv):
        for widthNum in range(widthDiv):
            widthCoord = widthNum * cellWidth + cellWidth / 2
            heightCoord = heightNum * cellHeight + cellHeight / 2

            radius = 10

            nodeCircle = canvas.create_oval(widthCoord - radius, heightCoord - radius,
                                            widthCoord + radius, heightCoord + radius, fill="black", outline="black")

            canvas.tag_bind(nodeCircle, "<Button-1>",
                            add_node)

    for key in graph:
        counter = n * 2
        widthCoord = (counter % widthDiv) * cellWidth + cellWidth / 2
        heightCoord = (counter // widthDiv) * cellHeight * 2 + cellHeight / 2

        tempText = canvas.create_text(
            widthCoord, heightCoord, font="Times 20", text=key, tag="node")

        radius = max(canvas.bbox(tempText)[
                     2] - canvas.bbox(tempText)[0], canvas.bbox(tempText)[3] - canvas.bbox(tempText)[1]) / 2 + 10

        nodeCircle = canvas.create_oval(widthCoord - radius, heightCoord - radius,
                                        widthCoord + radius, heightCoord + radius, fill="black", tag="node")

        nodeDict[key] = (nodeCircle, tempText)

        coordDict[key] = (widthCoord, heightCoord, radius)

        n += 1

    # creating the edges
    edgeList = edge_list(graph)

    for edge in edgeList:
        # math if on same level
        x0, y0, r0 = coordDict[edge[1]]
        x1, y1, r1 = coordDict[edge[2]]

        if y0 == y1:
            medianX, medianY = (x0 + x1)/2, (y0 + y1)/2
            centerCircleX, centerCircleY = medianX, medianY - abs(
                medianX - x0) * math.sqrt(3)/3
            bigR = abs(medianX - x0) * math.sqrt(3)/3 * 2

            arc = canvas.create_arc(centerCircleX - bigR, centerCircleY - bigR,
                                    centerCircleX + bigR, centerCircleY + bigR, start=210, extent=120, style=tkinter.ARC, tag=str((edge[1], edge[2])))

            text = canvas.create_text(centerCircleX, centerCircleY +
                                      bigR, text=str(edge[0]), fill="spring green")

            canvasEdgesDict[(edge[1], edge[2])] = (arc, text, True)
        else:
            line = canvas.create_line(x0, y0, x1, y1)

            text = canvas.create_text(
                (x0 + x1)/2, (y0 + y1)/2, text=str(edge[0]), fill="spring green")

            canvasEdgesDict[(edge[1], edge[2])] = (line, text, False)

    for key in graph:
        (nodeCircle, tempText) = nodeDict[key]
        canvas.tag_raise(nodeCircle)
        canvas.tag_raise(tempText)
        x0, y0, x1, y1 = canvas.coords(nodeCircle)
        invsCircle = canvas.create_oval(
            canvas.coords(nodeCircle), fill="", outline="", tag="node")
        invsNodeDict[invsCircle] = key
        canvas.tag_bind(invsCircle, "<Button-1>",
                        node_clicked)

        canvas.tag_bind(invsCircle, "<Button-2>",
                        remove_node)


def clear_canvas():
    global afterList

    for method in afterList:
        main.after_cancel(method)
    afterList = []
    for key in canvasEdgesDict:
        arc, text, isArc = canvasEdgesDict[key]

        if isArc:
            canvas.itemconfig(arc, outline="white")
        else:
            canvas.itemconfig(arc, fill="white")
    for key in nodeDict:
        nodeCircle, nodeText = nodeDict[key]

        canvas.itemconfig(nodeCircle, outline="white")

        canvas.itemconfig(nodeText, fill="white")


def run_prims(viewTimeEntry):
    global count

    viewTime = int(float(viewTimeEntry.get()) * 1000)
    clear_canvas()
    prims(tempGraphFixed, viewTime)


def run_kruskal(viewTimeEntry):
    global count

    viewTime = int(float(viewTimeEntry.get()) * 1000)
    count = 0
    clear_canvas()
    kruskal(tempGraphFixed, viewTime)


# only add arc when get value
def add_arc_with_value(value, nodeName, secondNodeName, popup):
    popup.destroy()
    tempGraphFixed[secondNodeName].append(
        (value, nodeName, secondNodeName))
    tempGraphFixed[nodeName].append((value, secondNodeName, nodeName))

    x0, y0, r0 = coordDict[nodeName]
    x1, y1, r1 = coordDict[secondNodeName]

    if y0 == y1:
        medianX, medianY = (x0 + x1)/2, (y0 + y1)/2
        centerCircleX, centerCircleY = medianX, medianY - abs(
            medianX - x0) * math.sqrt(3)/3
        bigR = abs(medianX - x0) * math.sqrt(3)/3 * 2

        arc = canvas.create_arc(centerCircleX - bigR, centerCircleY - bigR,
                                centerCircleX + bigR, centerCircleY + bigR, start=210, extent=120, style=tkinter.ARC, tag=str((nodeName, secondNodeName)))

        canvas.tag_lower(arc)

        text = canvas.create_text(centerCircleX, centerCircleY +
                                  bigR, text=str(value), fill="spring green")

        canvasEdgesDict[(nodeName, secondNodeName)] = (arc, text, True)
    else:
        line = canvas.create_line(x0, y0, x1, y1)

        text = canvas.create_text(
            (x0 + x1)/2, (y0 + y1)/2, text=str(value), fill="spring green")

        canvas.tag_lower(line)

        canvasEdgesDict[(nodeName, secondNodeName)
                        ] = (line, text, False)


def check_if_connected():
    # only needed for prims
    pass

# add an arc


def about_prims():

    popup = tkinter.Toplevel(main)

    popup.title("About Prim's Algorithm")

    popup.resizable(False, False)

    label = tkinter.Label(popup, text='''Prim's algorithm only works for connected graphs.
    (i.e, there exists a path between any two nodes.)
    
    Prim's algorithm works by visitng first an arbitrary node, then choosing a the edge
    with the least value that leads to a new node that has not been visited.
    
    The yellow-colored edges are edges being added to the list of nodes to visit,
    while the purple-colored edges are edges that are part of the minimum spanning tree.
    The red-colored edges are edges that are being currently processed but cannot be 
    added to the minimum-spanning tree.
    Lastly, the blue-colored node is the current node being processed with its
    neighboring edges added.
    
    Prim's algorithm is a little more complicated to visualise here than Kruskal's.''')
    label.pack()


def about_kruskals():

    popup = tkinter.Toplevel(main)

    popup.title("About Kruskal's Algorithm")

    popup.resizable(False, False)

    label = tkinter.Label(popup, text='''Kruskal's algorithm works by first sorting the edges
    by least weight. Then, for each edge, in order by lowest eight, it adds that
    edge if it adding it does not form a cycle in the graph.
    
    In the representation, the yellow-colored line is the current line being processed,
    while the purple-colored lines are the lines that are part of the minimum spanning tree.''')
    label.pack()


def how_to_use():

    popup = tkinter.Toplevel(main)

    popup.title("How to use")

    popup.resizable(False, False)

    label = tkinter.Label(popup, text='''This is a simple program designed to visualize
    Prim's and Kruskal's algorithm for creating minimuim spanning trees.
    
    To use, left click on any of the black circles, whcih represent coordinates, to create a node.
    You can delete nodes by right clicking on them. 
    
    Drag a node to another and enter a value to create an edge.
    
    Click the Run Prims and Run Kruskal Buttons to start the algorithms.
    
    Information on what the colors represent and more about the general algorithm is available with the
    "About Prim's" and "About Kruskal" Buttons.''')
    label.pack()


def add_arc(event):
    global nodeClicked

    nodeId = event.widget.find_withtag('current')
    if nodeId:
        if nodeId[0] in invsNodeDict and nodeClicked:
            secondNodeName = invsNodeDict[nodeId[0]]
            if nodeName != secondNodeName:
                getValue(nodeName, secondNodeName)

    nodeClicked = False


def create_basic_layout():
    viewTimeText = tkinter.Label(
        main, text="Enter how long each step should take (seconds):")
    viewTimeText.grid(row=0)

    viewTimeEntry = tkinter.Entry(main, width=50)
    viewTimeEntry.grid(row=0, column=1, columnspan=2)
    viewTimeEntry.insert(0, "1")

    primsButton = tkinter.Button(
        main, text="Run Prim's", command=lambda: run_prims(viewTimeEntry))
    kruskalButton = tkinter.Button(
        main, text="Run Kruskal", command=lambda: run_kruskal(viewTimeEntry))
    clearCanvasButton = tkinter.Button(
        main, text="Clear", command=clear_canvas)

    primsButton.grid(row=1, column=0)
    kruskalButton.grid(row=1, column=1)
    clearCanvasButton.grid(row=1, column=2)

    aboutPrims = tkinter.Button(
        main, text="About Prim's", command=about_prims)
    aboutKruskal = tkinter.Button(
        main, text="About Kruskal", command=about_kruskals)
    howToUse = tkinter.Button(
        main, text="Clear", command=how_to_use)

    aboutPrims.grid(row=2, column=0)
    aboutKruskal.grid(row=2, column=1)
    howToUse.grid(row=2, column=2)


if __name__ == "__main__":
    # weighted undirected graph
    # Each vertex SHOULD BE edge list w/ (weight, vertex) => messed up
    tempGraph = {
        "a": [("d", 3), ("c", 3), ("b", 2)],
        "b": [("a", 2), ("c", 4), ("e", 3)],
        "c": [("a", 3), ("b", 4), ("e", 1), ("d", 5), ("f", 6)],
        "d": [("a", 3), ("c", 5), ("f", 7)],
        "e": [("c", 1), ("b", 3), ("f", 8)],
        "f": [("d", 7), ("c", 6), ("e", 8), ("g", 9)],
        "g": [("f", 9)]
    }

    # to fix for prims => heapsort
    tempGraphFixed = {}

    for key in tempGraph:
        tempGraphFixed[key] = []
        for edge in tempGraph[key]:
            tempGraphFixed[key].append((edge[1], edge[0], key))

    create_basic_layout()
    create_basic_graph(tempGraphFixed)

    canvas.bind("<ButtonRelease-1>", add_arc)

tkinter.mainloop()
