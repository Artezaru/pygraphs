"""
.. _sphx_glr__gallery_dijkstra.py:


Dijkstra Example
=====================================================================================

.. contents:: Table of Contents
   :local:
   :depth: 2
   :backlinks: top

This example demonstrates the Breadth-First Search (BFS) algorithm on a simple :class:`pygraphs.Graph`.
The BFS algorithm explores the vertices of a graph in layers, starting from a given source vertex
and visiting all its neighbors before moving on to the next layer of vertices.

"""

# %%
# Define the graphs
# --------------------------------------------------------------------------------
#
# Create a simple disconnected graph of 7 vertices
#
# .. figure:: /_static/weighted_graph.png
#     :align: center
#     :width: 50%

#     Disconnected and weighted graph with 7 vertices for Dijkstra example.
#     Distance from vertex 0 to vertex 4 is 4.8.
#
# And a directed graph of 7 vertices
#
# .. figure:: /_static/weighted_graph_directed.png
#     :align: center
#     :width: 50%

#     Directed graph with 7 vertices for Dijkstra example. Distance from vertex 2 to
#     vertex 0 is 2.7.

from pygraphs import Graph

graph = [
    [(1, 1.2), (2, 0.2)],
    [(0, 1.2), (2, 1.5)],
    [(0, 0.2), (1, 1.5), (3, 3.2)],
    [(2, 3.2), (4, 1.4)],
    [(3, 1.4)],
    [(6, 2.3)],
    [(5, 2.3)],
]
undirected_graph = Graph.from_adjacency(graph)
print(undirected_graph.is_directed())  # False

graph = graph = [
    [(1, 1.2), (2, 0.2)],
    [(0, 1.2), (2, 1.5)],
    [(1, 1.5), (3, 3.2)],
    [(2, 1.4), (4, 1.4)],
    [(3, 1.4)],
    [(6, 2.3)],
    [],
]
directed_graph = Graph.from_adjacency(graph)
print(directed_graph.is_directed())  # True

# %%
# Dijkstra Examples
# --------------------------------------------------------------------------------
#
# Dijkstra Distances
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Computes shortest distances from a source vertex to all other vertices.
# Unreachable vertices have distance -1. (see also :func:`pygraphs.dijkstra_distances`)

from pygraphs import dijkstra_distances

start_vertex = 0
distances = dijkstra_distances(undirected_graph, start_vertex)
print(distances)  # Expected [0.0, 1.2, 0.2, 3.4, 4.8, -1.0, -1.0]

start_vertex = 2
distances = dijkstra_distances(directed_graph, start_vertex)
print(distances)  # Expected [2.7, 1.5, 0.0, 3.2, 4.6, -1.0, -1.0]


# %%
# Dijkstra Shortest Path
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Returns the minimum-cost path between a source and a target vertex. (see also :func:`pygraphs.dijkstra_shortest_path`)

from pygraphs import dijkstra_shortest_path

start_vertex = 0
end_vertex = 4
shortest_path = dijkstra_shortest_path(undirected_graph, start_vertex, end_vertex)
print(shortest_path)  # Expected [0, 2, 3, 4]

start_vertex = 2
end_vertex = 0
shortest_path = dijkstra_shortest_path(directed_graph, start_vertex, end_vertex)
print(shortest_path)  # Expected [2, 1, 0]


# %%
# Dijkstra Shortest Distance
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Returns the total minimum cost between two vertices. (see also :func:`pygraphs.dijkstra_shortest_distance`)

from pygraphs import dijkstra_shortest_distance

start_vertex = 0
end_vertex = 4
distance = dijkstra_shortest_distance(undirected_graph, start_vertex, end_vertex)
print(distance)  # Expected 4.8

start_vertex = 2
end_vertex = 0
distance = dijkstra_shortest_distance(directed_graph, start_vertex, end_vertex)
print(distance)  # Expected 2.7


# %%
# Dijkstra Matrix
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Computes the all-pairs shortest path matrix using Dijkstra. (see also :func:`pygraphs.dijkstra_matrix`)

from pygraphs import dijkstra_matrix

matrix = dijkstra_matrix(undirected_graph)
print(matrix)

# Expected output:
# adjacency_matrix (shape=(7x7)):
# [[ 0.0  1.2  0.2  3.4  4.8 -1.0 -1.0]
#  [ 1.2  0.0  1.4  4.6  6.0 -1.0 -1.0]
#  [ 0.2  1.4  0.0  3.2  4.6 -1.0 -1.0]
#  [ 3.4  4.6  3.2  0.0  1.4 -1.0 -1.0]
#  [ 4.8  6.0  4.6  1.4  0.0 -1.0 -1.0]
#  [-1.0 -1.0 -1.0 -1.0 -1.0  0.0  2.3]
#  [-1.0 -1.0 -1.0 -1.0 -1.0  2.3  0.0]]

matrix = dijkstra_matrix(directed_graph)
print(matrix)

# Expected output:
# adjacency_matrix (shape=(7x7)):
# [[ 0.0  1.2  0.2  3.4  4.8 -1.0 -1.0]
#  [ 1.2  0.0  1.4  4.6  6.0 -1.0 -1.0]
#  [ 0.2  1.4  0.0  3.2  4.6 -1.0 -1.0]
#  [ 1.6  2.8  1.4  0.0  1.4 -1.0 -1.0]
#  [ 3.0  4.2  2.8  1.4  0.0 -1.0 -1.0]
#  [-1.0 -1.0 -1.0 -1.0 -1.0  0.0  2.3]
#  [-1.0 -1.0 -1.0 -1.0 -1.0 -1.0  0.0]]

# %%
# Dijkstra k-annulus
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Returns nodes whose shortest path distance is between an inner and outer bound. (see also :func:`pygraphs.dijkstra_k_annulus`)

from pygraphs import dijkstra_k_annulus

start_vertex = 0
inner_distance = 0.1
outer_distance = 4.0

neighborhood = dijkstra_k_annulus(
    undirected_graph, start_vertex, inner_distance, outer_distance
)
print(neighborhood)  # Expected [1, 2, 3]


# %%
# Dijkstra k-disk
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# Returns all nodes within a given distance threshold. (see also :func:`pygraphs.dijkstra_k_disk`)

from pygraphs import dijkstra_k_disk

start_vertex = 0
distance = 4.0

neighborhood = dijkstra_k_disk(undirected_graph, start_vertex, distance)
print(neighborhood)  # Expected [0, 1, 2, 3]
