- AdjacencyList: ``List[List[Integral]]]``: A list of lists, where
  the outer list has a length equal to the number of vertices in the graph, and each inner
  list contains the neighbors (i.e., ``[v1, v2, ...]``) of the corresponding vertex (from
  outer vertex to inner vertex). For a weighted graph, the form ``List[List[Tuple[Integral, Real]]]``
  is used where the inner lists contain tuples of the form :math:`(v, w)`,
  where :math:`v` is a neighbor vertex and :math:`w` is the weight of the edge
  connecting the vertex to its neighbor. To store more than weight, the form
  ``List[List[Tuple[Integral, Dict[str, Any]]]]`` is used.