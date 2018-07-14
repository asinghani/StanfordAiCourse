from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString

from shapely.ops import cascaded_union
from AdjacencyMatrixGraph import AdjacencyMatrixGraph
from Graph import Node

def makeVisGraph(obstacles):
    obstaclePolys = []
    for obstacle in obstacles:
        obstaclePolys.append(Polygon(obstacle))

    combined = cascaded_union(obstaclePolys)
    nodes = []

    if type(combined) is Polygon:
        # single obj
        nodes.extend(list(combined.exterior.coords))
    else:
        # multiple
        for polygon in combined:
            nodes.extend(list(polygon.exterior.coords))

    nodes = list(set(nodes))
    graph = AdjacencyMatrixGraph(len(nodes))
    graph.nodes = [Node(data = str((n[0], n[1]))) for n in nodes]

    for i in range(len(nodes)):
        node1 = nodes[i]
        for i2 in range(len(nodes)):
            node2 = nodes[i2]

            if node1 == node2:
                continue

            line = LineString([node1, node2])

            intersect = False
            for obs in combined:
                if obs.contains(line) or obs.crosses(line) or obs.within(line):
                    intersect = True
                    break

            if not intersect:
                graph.addEdge(graph.nodes[i], graph.nodes[i2])

    graph.visualizeGraph()


if __name__ == "__main__":
    polys = [[(0, 0), (0, 20), (20, 20), (20, 0)],
             [(35, 35), (25, 35), (25, 25), (35, 25)]]

    makeVisGraph(polys)
    pass
