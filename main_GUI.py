import heapq
import math
import Prims_And_Kruskals
import tkinter

main = tkinter.Tk()
main.title("Graphs Visualization")
main.resizable(False, False)

width, height = 960, 720

canvas = tkinter.Canvas(main, width=width, height=height)
canvas.grid(row=2, column=0, columnspan=3)

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


# one pass of heappush
def heappush_kruskal(counter, limit, edgeList, priorityQueue, viewTime):
    if counter < limit:

        edge = edgeList[counter]
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

        heappushKruskal = main.after(viewTime, lambda: heappush_kruskal(
            counter + 1, limit, edgeList, priorityQueue, viewTime))
        afterList.append(heappushKruskal)

# implementation of prims


def one_turn_prims(graph, visited, priorityQueue, viewTime):
    leastNum = heapq.heappop(priorityQueue)
    numEdges = 0
    if leastNum[1] not in visited:
        # color edge that is part of dst
        if (leastNum[1], leastNum[2]) in canvasEdgesDict:
            arc, text, isArc = canvasEdgesDict[(leastNum[1], leastNum[2])]
            if isArc:
                canvas.itemconfig(arc, outline="purple1")
            else:
                canvas.itemconfig(arc, fill="purple1")
        elif (leastNum[2], leastNum[1]) in canvasEdgesDict:
            arc, text, isArc = canvasEdgesDict[(leastNum[2], leastNum[1])]
            if isArc:
                canvas.itemconfig(arc, outline="purple1")
            else:
                canvas.itemconfig(arc, fill="purple1")

        mst.append(leastNum)

        nodeCircle, nodeText = nodeDict[leastNum[1]]
        canvas.itemconfig(nodeCircle, outline="RoyalBlue1")

        numEdges = len(graph[leastNum[1]])
        heappushKruskal = main.after(viewTime,
                                     lambda: heappush_kruskal(0, numEdges, graph[leastNum[1]], priorityQueue, viewTime))
        changeColor = main.after(viewTime * (numEdges + 1),
                                 lambda: canvas.itemconfig(nodeCircle, outline="white"))

        afterList.append(heappushKruskal)
        afterList.append(changeColor)

        visited.add(leastNum[1])

    if priorityQueue:
        nextTurn = main.after(viewTime * (numEdges + 1), lambda: one_turn_prims(
            graph, visited, priorityQueue, viewTime))

        afterList.append(nextTurn)


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

    heappush_kruskal(0, numEdges, graph[initialNode], priorityQueue, viewTime)

    starting = main.after(viewTime * (numEdges),
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
                                            widthCoord + radius, heightCoord + radius, fill="white")

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
                                      bigR, text=str(edge[0]), fill="turquoise1")

            canvasEdgesDict[(edge[1], edge[2])] = (arc, text, True)
        else:
            line = canvas.create_line(x0, y0, x1, y1)

            text = canvas.create_text(
                (x0 + x1)/2, (y0 + y1)/2, text=str(edge[0]), fill="turquoise1")

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


def add_arc(event):
    global nodeClicked

    nodeId = event.widget.find_withtag('current')
    if nodeId:
        if nodeId[0] in invsNodeDict and nodeClicked:
            secondNodeName = invsNodeDict[nodeId[0]]
            value = 5
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
                                          bigR, text=str(value), fill="turquoise1")

                canvasEdgesDict[(nodeName, secondNodeName)] = (arc, text, True)
            else:
                line = canvas.create_line(x0, y0, x1, y1)

                text = canvas.create_text(
                    (x0 + x1)/2, (y0 + y1)/2, text=str(value), fill="turquoise1")

                canvas.tag_lower(line)

                canvasEdgesDict[(nodeName, secondNodeName)
                                ] = (line, text, False)

    nodeClicked = False


def create_basic_layout():
    viewTimeText = tkinter.Label(
        main, text="Enter how long each step should take (seconds):")
    viewTimeText.grid(row=0)

    viewTimeEntry = tkinter.Entry(main, width=50)
    viewTimeEntry.grid(row=0, column=1, columnspan=2)
    viewTimeEntry.insert(0, "1")

    primsButton = tkinter.Button(
        main, text="Run Prims", command=lambda: run_prims(viewTimeEntry))
    kruskalButton = tkinter.Button(
        main, text="Run Kruskal", command=lambda: run_kruskal(viewTimeEntry))
    clearCanvasButton = tkinter.Button(
        main, text="Clear", command=clear_canvas)

    primsButton.grid(row=1, column=0)
    kruskalButton.grid(row=1, column=1)
    clearCanvasButton.grid(row=1, column=2)


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
