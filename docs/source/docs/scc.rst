Strongly Connected Components (SCC)
-----------------------------------

.. currentmodule:: pygraphs

Strongly connected components (SCC) are defined for **directed graphs**.

A strongly connected component is a maximal set of vertices such that every vertex
is reachable from every other vertex in both directions.

In other words, for any vertices u and v in the same component:
there exists a path from u to v **and** a path from v to u.

SCCs are used to analyze cyclic structure in directed graphs and to decompose a graph
into irreducible components.

Two algorithms are provided to compute strongly connected components:

- **Tarjan's algorithm**: a single-pass DFS algorithm using low-link values.
- **Kosaraju's algorithm**: a two-pass DFS algorithm based on graph reversal.

Both methods run in :math:`O(V + E)` time.

.. autosummary::
   :toctree: _generated/

   tarjan_components
   kosaraju_components