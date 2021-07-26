import heapq

# implementation of prims


def prims(graph):
    visited = set()

    mst = []

    initialNode = "a"
    priorityQueue = []
    for edge in graph[initialNode]:
        heapq.heappush(priorityQueue, edge)

    visited.add(initialNode)

    while priorityQueue:
        leastNum = heapq.heappop(priorityQueue)
        if leastNum[1] not in visited:
            mst.append(leastNum)
            for edge in graph[leastNum[1]]:
                heapq.heappush(priorityQueue, edge)
            visited.add(leastNum[1])

    print(mst)
    return mst


def kruskal(graph):

    sortedGraph = []

    mst = []

    usedEdges = set()

    for key in graph:
        for edge in graph[key]:
            if (edge[1], key) not in usedEdges and (key, edge[1]) not in usedEdges:
                usedEdges.add((edge[1], edge[2]))
                sortedGraph.append(edge)

    sortedGraph.sort(key=lambda x: x[0])

    # dict of "ids" too quickly find if cycle
    dsu = {}
    counter = 0
    for key in graph:
        dsu[key] = counter
        counter += 1

    # iterate through sorted graph
    for edge in sortedGraph:
        length, first, second = edge

        if dsu[first] != dsu[second]:
            idToChange = dsu[second]
            idToBe = dsu[first]
            for key in dsu:
                if dsu[key] == idToChange:
                    dsu[key] = idToBe
            mst.append(edge)

    print(mst)
    return mst


if __name__ == "__main__":
    # weighted undirected graph
    # Each vertex has edge list w/ (weight, vertex)
    tempGraph = {
        "a": [("d", 3), ("c", 3), ("b", 2)],
        "b": [("a", 2), ("c", 4), ("e", 3)],
        "c": [("a", 3), ("b", 4), ("e", 1), ("d", 5), ("f", 6)],
        "d": [("a", 3), ("c", 5), ("f", 7)],
        "e": [("c", 1), ("b", 3), ("f", 8)],
        "f": [("d", 7), ("c", 6), ("e", 8), ("g", 9)],
        "g": [("f", 9)]
    }

    # for prims
    tempGraphFixed = {}

    for key in tempGraph:
        tempGraphFixed[key] = []
        for edge in tempGraph[key]:
            tempGraphFixed[key].append((edge[1], edge[0], key))

    prims(tempGraphFixed)
    kruskal(tempGraphFixed)
