import time
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

# list of pending after methods
afterList = []

# dict of edges to remove and edit
canvasEdgesDict = {}

mst = []

count = 0

# kruskals


def one_turn_kruskal(dsu, sortedGraph, viewTime):
    global count
    print(count, "coount")
    edge = sortedGraph[count]

    length, first, second = edge

    arc = canvasEdgesDict[(edge[1], edge[2])]

    canvas.itemconfig(arc, outline="gold")
    print(edge, viewTime, arc)

    if dsu[first] != dsu[second]:
        idToChange = dsu[second]
        idToBe = dsu[first]
        for key in dsu:
            if dsu[key] == idToChange:
                dsu[key] = idToBe
        mst.append(edge)
    else:
        returnCanvas = canvas.after(viewTime,
                                    lambda: canvas.itemconfig(arc, outline="white"))

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

    print(sortedGraph)

    # iterate through sorted graph
    counter = 0
    for edge in sortedGraph:

        moveCanvas = canvas.after(viewTime * counter,
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

# create the outline of the graph in tkinter


def create_basic_graph(graph):

    # dict of (coords, radius)
    coordDict = {}

    widthDiv, heightDiv = 13, 9

    cellWidth, cellHeight = width / widthDiv, height / heightDiv

    # radius = min(width/(2 * widthDiv), height/(2 * heightDiv)) - 40

    numNodes = len(graph)

    n = 0

    for key in graph:
        counter = n * 2
        widthCoord = (counter % widthDiv) * cellWidth + cellWidth / 2
        heightCoord = (counter // widthDiv) * cellHeight * 2 + cellHeight / 2

        tempText = canvas.create_text(
            widthCoord, heightCoord, font="Times 20", text=key)

        radius = max(canvas.bbox(tempText)[
                     2] - canvas.bbox(tempText)[0], canvas.bbox(tempText)[3] - canvas.bbox(tempText)[1]) / 2 + 10

        canvas.create_oval(widthCoord - radius, heightCoord - radius,
                           widthCoord + radius, heightCoord + radius)

        coordDict[key] = (widthCoord, heightCoord, radius)

        n += 1

    # creating the edges
    edgeList = edge_list(graph)
    print(edgeList)
    for edge in edgeList:
        x0, y0, r0 = coordDict[edge[1]]
        x1, y1, r1 = coordDict[edge[2]]
        medianX, medianY = (x0 + x1)/2, (y0 + r0 + y1 + r1)/2
        centerCircleX, centerCircleY = medianX, medianY - abs(
            medianX - x0) * math.sqrt(3)/3
        bigR = abs(medianX - x0) * math.sqrt(3)/3 * 2

        arc = canvas.create_arc(centerCircleX - bigR, centerCircleY - bigR,
                                centerCircleX + bigR, centerCircleY + bigR, start=210, extent=120, style=tkinter.ARC, tag=str((edge[1], edge[2])))

        text = canvas.create_text(centerCircleX, centerCircleY +
                                  bigR, text=str(edge[0]), fill="turquoise1")

        canvasEdgesDict[(edge[1], edge[2])] = arc


def clear_canvas():
    for method in afterList:
        main.after_cancel(method)
    for key in canvasEdgesDict:
        arc = canvasEdgesDict[key]
        canvas.itemconfig(arc, outline="white")


def run_kruskal(viewTimeEntry):
    global count

    viewTime = int(float(viewTimeEntry.get()) * 1000)
    count = 0
    clear_canvas()
    kruskal(tempGraphFixed, viewTime)


def create_basic_layout():
    viewTimeText = tkinter.Label(
        main, text="Enter how long each step should take (seconds):")
    viewTimeText.grid(row=0)

    viewTimeEntry = tkinter.Entry(main, width=50)
    viewTimeEntry.grid(row=0, column=1, columnspan=2)

    primsButton = tkinter.Button(
        main, text="Run Prims")
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

tkinter.mainloop()
