Depth-First Search (DFS)
------------------------

.. currentmodule:: pygraphs

The depth-first search (DFS) algorithm is implemented to
traverse the graph and explore vertices by going as deep as possible before backtracking.

The DFS algorithm can be used on both **directed** and **undirected** graphs.

For **unweighted graphs**, DFS is not used to compute shortest paths, but rather for:
connected components, reachability, and graph traversal structures.

All DFS functions are convenience wrappers built on top of :func:`pygraphs.dfs`.

.. autosummary::
   :toctree: _generated/

   dfs
   dfs_is_reachable
   dfs_reachable
   dfs_components
