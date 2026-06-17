Dijkstra Algorithm
------------------

.. currentmodule:: pygraphs

The Dijkstra algorithm is implemented to compute shortest paths in
**weighted graphs with non-negative edge weights**.

It explores the graph starting from a source vertex and progressively
expands the set of visited vertices using a priority queue (min-heap),
always selecting the vertex with the smallest known distance.

The algorithm is used to compute shortest paths in weighted graphs
where all edge weights are non-negative.

Unlike BFS, which assumes unit weights, Dijkstra takes edge weights into account.

All Dijkstra functions are convenience wrappers built on top of
:func:`pygraphs.dijkstra`.

.. note::

   The algorithm assumes all edge weights are **non-negative**.
   Negative weights will produce incorrect results.

.. autosummary::
   :toctree: _generated/

   dijkstra
   dijkstra_distances
   dijkstra_shortest_path
   dijkstra_shortest_distance
   dijkstra_matrix
   dijkstra_k_annulus
   dijkstra_k_disk