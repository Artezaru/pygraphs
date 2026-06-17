- Edges: ``List[Tuple[Integral, Integral]]``: A list of tuples, 
  where each tuple represents an edge :math:`(u, v)` in the graph (from vertex :math:`u`
  to vertex :math:`v`). For a undirected graph consider converting in :class:`pygraphs.Graph`
  class and use the ``to_undirected`` method to duplicate :math:`(u, v)` into :math:`(u, v)`
  and :math:`(v, u)`. For a weighted graph, the form ``List[Tuple[Integral, Integral, Real]]``
  containing :math:`(u, v, w)` is used, where :math:`u` and :math:`v` are the vertices connected by 
  the edge and :math:`w` is the weight of the edge. To store more than weight, the form 
  ``List[Tuple[Integral, Integral, Dict[str, Any]]]`` is used.
  