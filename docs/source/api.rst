API Reference
==============

.. currentmodule:: pygraphs

.. contents:: API Reference
   :local:

This section contains a detailed description of the functions, modules, and objects included in ``pygraphs``. 


Graphs
------

The three main graph representations in the package are :

.. include:: /_static/rstdoc/adjacency_list_representation.rst

.. include:: /_static/rstdoc/edges_representation.rst

.. include:: /_static/rstdoc/graph_representation.rst


Graph Class
^^^^^^^^^^^^

- :class:`pygraphs.Graph`: The main class representing a graph and validating the graph structure. 
- :doc:`Conversion Functions <docs/convertion>` - Functions to convert between different graph 
  representations (e.g., adjacency list, edge list, graph dictionary format).

.. toctree::
   :maxdepth: 1
   :hidden:

   docs/graph
   docs/convertion

A graph is :

- **weighted/unweighted** if it has edges with weights (i.e., numerical values representing the strength or cost of the connection between vertices).
  In the :class:`pygraphs.Graph` class, all graphs are stored in a weighted format but the weights can be set to 
  a default value (e.g., 1) for unweighted graphs.

- **directed/undirected** if the edges have a direction (i.e., they go from one vertex to another) or not. 
  In the :class:`pygraphs.Graph` class, all graphs are stored in a directed format but undirected graphs 
  can be represented by adding edges in both directions. The weights must be the same for both directions 
  in the case of undirected graphs otherwise the graph will be considered as directed.

- **weight symmetric** (for directed graphs) if for both two-way edges between vertices :math:`u` and :math:`v`, 
  the weights are the same (i.e., :math:`w(u, v) = w(v, u)` if :math:`(u, v)` and :math:`(v, u)` are both present). 


Algorithms
---------------------------

- :doc:`Breadth-First Search (BFS) <docs/bfs>` - A graph traversal algorithm that explores the graph level by level starting from a source vertex. It is used to find the shortest path in an unweighted graph and to explore all reachable nodes efficiently.
- :doc:`Depth-First Search (DFS) <docs/dfs>` - A graph traversal algorithm that explores as far as possible along each branch before backtracking. It is useful for connectivity checks, cycle detection, and structural analysis of graphs.
- :doc:`Strongly Connected Components (SCC) <docs/scc>` - A decomposition of a directed graph into maximal subsets of vertices where every vertex is reachable from every other vertex in the same subset. It is used to analyze dependency structures and directed graph topology (e.g., via Tarjan’s or Kosaraju’s algorithm).
- :doc:`Dijkstra <docs/dijkstra>` - An algorithm for finding the shortest paths from a single source vertex to all other vertices in a weighted graph with non-negative edge weights. It is widely used in routing, GPS navigation, and network optimization.

.. toctree::
   :maxdepth: 1
   :hidden:

   docs/bfs
   docs/dfs
   docs/scc
   docs/dijkstra