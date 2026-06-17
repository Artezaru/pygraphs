Create a Graph from other structures
=====================================

.. currentmodule:: pygraphs

The following functions are provided to convert between different graph representations. 
These functions can be used to create a graph from an adjacency list or an edge list,
and to convert into graph dictionary format.

The three main graph representations are:

.. include:: /_static/rstdoc/adjacency_list_representation.rst

.. include:: /_static/rstdoc/edges_representation.rst

.. include:: /_static/rstdoc/graph_representation.rst

.. autosummary::
   :toctree: _generated/

   adjacency_list_to_graph
   edges_list_to_graph
   graph_to_adjacency_list
   graph_to_edges_list
   adjacency_list_to_edges_list
   edges_list_to_adjacency_list
