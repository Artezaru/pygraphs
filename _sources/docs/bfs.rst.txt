Breadth-First Search (BFS)
---------------------------

.. currentmodule:: pygraphs

The breadth-first search (BFS) algorithm is implemented to 
traverse the graph and find the shortest path between vertices.
The BFS algorithm is intented to be used on **unweighted** graphs.

For **unweighted** graphs, the distance between two vertices 
is defined as the number of edges in the shortest path connecting them.

All BFS functions are convenience wrappers built on top of :func:`pygraphs.bfs`.

.. autosummary::
   :toctree: _generated/
   :caption: Core

   bfs
   bfs_distances
   bfs_shortest_path
   bfs_shortest_distance
   bfs_is_reachable
   bfs_matrix
   bfs_reachable
   bfs_components
   bfs_k_annulus
   bfs_k_disk
   bfs_k_ring
