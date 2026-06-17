"""
pygraphs - Python graphs library to perform Dijkstra, DFS, Dijkstra, and more.
Copyright (C) 2026 Artezaru, artezaru.github@proton.me

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Tuple
from numbers import Integral, Real
from .graph import Graph

from heapq import heappush, heappop
from .exeptions import assert_valid_graph_weights


def dijkstra(
    graph: Graph,
    start: Integral,
    *,
    max_distance: Optional[Real] = None,
    weight_key: str = "weight",
    _skip_check: bool = False,
) -> Tuple[Dict[int, int], Dict[int, float]]:
    r"""
    [core function] Perform a Dijkstra algorithm to compute the shortest path distances from
    a starting vertex to all other vertices in a **weighted** graph, and to keep track
    of the parent vertices for each visited vertex.

    .. warning::

        No tests are performed to check if the input graph is valid (e.g., if the graph
        contains self-loops, if the graph contains invalid vertex indices, ...).
        The behavior of the function is undefined if the input graph is not valid.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index.

    max_distance : Optional[Real], optional (default: ``None``)
        The maximum distance to search. All vertices
        that are not reachable within this distance will be ignored.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.


    Returns
    -------
    parents: Dict[int, int]
        A dictionary mapping each visited vertex index to its parent vertex index in the Dijkstra tree.
        The starting vertex will have a parent of None.

    distances: Dict[int, float]
        A dictionary mapping each visited vertex index to its shortest path distance from the
        starting vertex. The starting vertex will have a distance of 0.


    Notes
    -----
    The function uses a Dijkstra approach to compute the shortest path distances, which is
    efficient for weighted graphs. The time complexity is :math:`O((V + E)\log V`, where :math:`V`
    is the number of vertices and :math:`E` is the number of edges in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distances from a starting vertex (0) to all other vertices in the graph.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Distance from vertex 0 to vertex 4 is 4.8.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        parent, distance = dijkstra(graph, start_vertex)
        print("Parent:", parent)
        print("Distance:", distance)

    .. code-block:: console

        Parent: {0: None, 1: 0, 2: 0, 3: 2, 4: 3}
        Distance: {0: 0, 1: 1.2, 2: 0.2, 3: 3.4, 4: 4.8}

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Distance from vertex 2 to
        vertex 0 is 2.7.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2

        parent, distance = dijkstra(graph, start_vertex)
        print("Parent:", parent)
        print("Distance:", distance)

    .. code-block:: console

        Parent: {2: None, 1: 2, 3: 2, 0: 1, 4: 3}
        Distance: {2: 0.0, 1: 1.5, 3: 3.2, 0: 2.7, 4: 4.6}

    """
    if not _skip_check:
        if not isinstance(graph, Graph):
            raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")

        if not isinstance(start, Integral):
            raise TypeError(f"start must be an integer. Got {type(start)}.")
        if start < 0 or start >= graph.n_vertices:
            raise ValueError(
                f"start must be an integer between 0 and n_vertices-1. Got {start}."
            )
        start = int(start)

        if max_distance is not None and (not isinstance(max_distance, Real)):
            raise TypeError(
                f"max_distance must be an real or None. Got {type(max_distance)}."
            )
        if max_distance is not None and max_distance < 0:
            raise ValueError(
                f"max_distance must be a non-negative float or None."
                f" Got {max_distance}."
            )
        if max_distance is not None:
            max_distance = float(max_distance)

        if not isinstance(weight_key, str):
            raise TypeError(f"weight_key must be a string. Got {type(weight_key)}.")

    # -- Dijkstra initialization --
    graph = graph._graph  # Dict[int, Dict[int, Dict[str, Any]]]
    if not _skip_check:
        assert_valid_graph_weights(graph=graph, weight_key=weight_key)

    distances: Dict[int, float] = {start: 0.0}
    parents: Dict[int, Optional[int]] = {start: None}
    heap = [(0.0, start)]  # (distance, node)

    # -- Dijkstra loop --
    while heap:
        dist_u, u = heappop(heap)

        # Skip outdated entries
        if dist_u != distances.get(u, float("inf")):
            continue

        # Optional pruning
        if max_distance is not None and dist_u > max_distance:
            continue

        for v, attrs in graph[u].items():
            weight = attrs.get(weight_key, 1.0)
            new_dist = dist_u + weight

            if max_distance is not None and new_dist > max_distance:
                continue

            if v not in distances or new_dist < distances[v]:
                distances[v] = new_dist
                parents[v] = u
                heappush(heap, (new_dist, v))

    return parents, distances


def dijkstra_distances(
    graph: Graph,
    start: Integral,
    *,
    max_distance: Optional[Real] = None,
    weight_key: str = "weight",
    _skip_check: bool = False,
) -> List[float]:
    r"""
    Compute shortest path distances from a source vertex to **all** reachable vertices
    using Dijkstra.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the Dijkstra.

    max_distance : Optional[Real], optional (default: ``None``)
        The maximum distance to search for in the Dijkstra. All vertices
        that are not reachable within this distance will be ignored.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.


    Returns
    -------
    List[float]
        A list of float representing the shortest path distances from the starting
        vertex to all other vertices in the graph.
        The length of the output list is equal to the number of vertices in the graph.
        Unreachable vertices have distance of ``-1.0``.


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.

    :func:`pygraphs.dijkstra_matrix`
        Compute the shortest path distance matrix for all pairs of vertices in the graph
        using Dijkstra.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distances from a starting vertex (0) to all other vertices in the graph.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Distance from vertex 0 to vertex 4 is 4.8.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_distances, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        distances = dijkstra_distances(graph, start_vertex)
        print(distances)

    .. code-block:: console

        [0.0, 1.2, 0.2, 3.4, 4.8, -1.0, -1.0]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Distance from vertex 2 to
        vertex 0 is 2.7.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_distances, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2

        distances = dijkstra_distances(graph, start_vertex)
        print(distances)

    .. code-block:: console

        [2.7, 1.5, 0.0, 3.2, 4.6, -1.0, -1.0]

    """
    _, distance_dict = dijkstra(
        graph,
        start,
        max_distance=max_distance,
        weight_key=weight_key,
        _skip_check=_skip_check,
    )
    n_vertices = graph.n_vertices
    return [distance_dict.get(i, -1.0) for i in range(n_vertices)]


def dijkstra_k_annulus(
    graph: Graph,
    start: Integral,
    inner_distance: Optional[Real],
    outer_distance: Optional[Real],
    *,
    weight_key: str = "weight",
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Return all vertices with distance in :math:`[k_1, k_2]`
    (ie :math:`\{v \in V | \text{dist}(i, v) \in [k_1, k_2]\}`) where :math:`k_1` and
    :math:`k_2` are the specified inner and outer distances.


    Parameters
    ----------
    graph : Graph
        An instance of the Graph class representing the graph to be traversed.

    start : Integral
        The starting vertex index for the Dijkstra.

    inner_distance : Optional[Real]
        The minimum distance :math:`k_1` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are at least this distance from the vertex.
        If None, there is no minimum distance and all vertices that are at
        least 0 distance from the vertex are included.

    outer_distance : Optional[Real]
        The maximum distance :math:`k_2` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are at most this distance from the vertex.
        If None, there is no maximum distance and all vertices that are reachable
        from the starting vertex are included.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.



    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices in the adjacency annulus
        of the starting vertex in the graph (i.e., the set of vertices that are between
        inner_distance and outer_distance from the starting vertex).


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.

    :func:`pygraphs.dijkstra_k_disk`
        Call this function with ``inner_distance = 0`` and ``outer_distance = k`` to extract the
        vertices in a adjacency disk of a starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and extract the vertices within
    distance range.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Vertices 1, 2 and 3 are the only vertices in the neighborhood of vertex
        0 for inner_distance = 0.1 and outer_distance = 4.0.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_annulus, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        inner_distance = 0.1
        outer_distance = 4.0

        neighborhood = dijkstra_k_annulus(graph, start_vertex, inner_distance, outer_distance)
        print(neighborhood)

    .. code-block:: console

        [1, 2, 3]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Vertices 1 and 3 are the only
        vertices in the neighborhood of vertex 2 for inner_distance = 1.0 and outer_distance = 3.5.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_annulus, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        inner_distance = 1.0
        outer_distance = 3.5

        neighborhood = dijkstra_k_annulus(graph, start_vertex, inner_distance, outer_distance)
        print(neighborhood)

    .. code-block:: console

        [1, 3]

    """
    if inner_distance is not None and not isinstance(inner_distance, Real):
        raise TypeError(f"inner_distance must be an float. Got {type(inner_distance)}.")
    if inner_distance is not None and inner_distance < 0:
        raise ValueError(
            f"inner_distance must be a non-negative float." f" Got {inner_distance}."
        )
    if inner_distance is not None:
        inner_distance = float(inner_distance)
    else:
        inner_distance = 0

    if outer_distance is not None and not isinstance(outer_distance, Real):
        raise TypeError(f"outer_distance must be an float. Got {type(outer_distance)}.")
    if outer_distance is not None and outer_distance < 0:
        raise ValueError(
            f"outer_distance must be a non-negative float." f" Got {outer_distance}."
        )
    if outer_distance is not None:
        outer_distance_dijkstra = float(outer_distance)
        outer_distance = float(outer_distance)
    else:
        outer_distance_dijkstra = None
        outer_distance = float("inf")

    if inner_distance > outer_distance:
        return []

    _, distance_dict = dijkstra(
        graph,
        start,
        max_distance=outer_distance_dijkstra,
        weight_key=weight_key,
        _skip_check=_skip_check,
    )
    return [
        v for v, d in distance_dict.items() if inner_distance <= d <= outer_distance
    ]


def dijkstra_k_disk(
    graph: Graph,
    start: Integral,
    distance: Integral,
    *,
    weight_key: str = "weight",
    self_neighborhood: bool = True,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Return all vertices with distance lower than :math:`k`
    (ie :math:`\{v \in V | \text{dist}(i, v) \leq k\}`) where :math:`k` is
    the specified distance.


    Parameters
    ----------
    graph : Graph
        An instance of the Graph class representing the graph to be traversed.

    start : Integral
        The starting vertex index for the Dijkstra.

    distance : Integral
        The adjacency radius :math:`k` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are within this distance from the vertex.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.

    self_neighborhood : bool, optional (default: ``True``)
        If True, the neighborhood of the vertex will include the vertex itself
        (i.e., the vertex will be considered as part of its own neighborhood).
        If False, the neighborhood of the vertex will not include the vertex
        itself.


    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices in the adjacency disk
        of the starting vertex in the graph (i.e., the set of vertices that are within
        the specified distance from the starting vertex).


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.

    :func:`pygraphs.dijkstra_k_annulus`
        Call this function with ``inner_distance = 0`` and ``outer_distance = k`` to extract the
        vertices in a adjacency annulus of a starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices extract the vertices within
    distance range.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Vertices 0, 1, 2 and 3 are the only vertices in the neighborhood of vertex
        0 for distance = 4.0.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        distance = 4.0

        neighborhood = dijkstra_k_disk(graph, start_vertex, distance)
        print(neighborhood)

    .. code-block:: console

        [0, 1, 2, 3]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Vertices 0, 1 and 3 are the only
        vertices in the neighborhood of vertex 2 for distance = 3.5.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        distance = 3.5

        neighborhood = dijkstra_k_disk(graph, start_vertex, distance)
        print(neighborhood)

    .. code-block:: console

        [0, 1, 3]

    """
    if not isinstance(self_neighborhood, bool):
        raise TypeError(
            f"self_neighborhood must be a boolean. Got {type(self_neighborhood)}."
        )

    if self_neighborhood:
        inner_distance = 0
    else:
        inner_distance = 1

    return dijkstra_k_annulus(
        graph,
        start,
        inner_distance,
        distance,
        weight_key=weight_key,
        _skip_check=_skip_check,
    )


def dijkstra_shortest_path(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    weight_key: str = "weight",
    max_distance: Optional[Real] = None,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Compute the shortest path from a starting vertex to an ending vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the Dijkstra.

    end: Integral
        The ending vertex index for the Dijkstra.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.

    max_distance : Optional[Real], optional (default: ``None``)
        The maximum distance to search for in the Dijkstra. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    List[int]
        A list of vertex indices representing the shortest path from the starting vertex
        to the ending vertex in the graph. If there is no path from the starting vertex
        to the ending vertex, an empty list is returned.


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    from a starting vertex (0) to an other vertex.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Shortest path from vertex 0 to
        vertex 4 is (0 -> 2 -> 3 -> 4).

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        shortest_path = dijkstra_shortest_path(graph, start_vertex, end_vertex)
        print(shortest_path)

    .. code-block:: console

        [0, 2, 3, 4]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Shortest path from vertex 2 to
        vertex 0 is (2 -> 1 -> 0).

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        end_vertex = 0

        shortest_path = dijkstra_shortest_path(graph, start_vertex, end_vertex)
        print(shortest_path)

    .. code-block:: console

        [2, 1, 0]

    """
    parent, distance_dict = dijkstra(
        graph,
        start,
        max_distance=max_distance,
        # stop_encounter=end, TODO: Optimizable ?
        weight_key=weight_key,
        _skip_check=_skip_check,
    )
    if end not in distance_dict:
        return []

    # -- Reconstruct path from end to start using parent dictionary --
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = parent[current_vertex]
    path.reverse()
    return path


def dijkstra_shortest_distance(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    weight_key: str = "weight",
    max_distance: Optional[Real] = None,
    _skip_check: bool = False,
) -> float:
    r"""
    Compute the shortest distance from a starting
    vertex to an ending vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the Dijkstra.

    end: Integral
        The ending vertex index for the Dijkstra.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.

    max_distance : Optional[Real], optional (default: ``None``)
        The maximum distance to search for in the Dijkstra. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    float
        The distance from starting vertex to ending vertex. Or ``-1.0`` if not reachable.


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.

    :func:`pygraphs.dijkstra_distances`
        Compute the shortest path distances
        from a starting vertex to all other vertices in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest distance
    from a starting vertex (0) to an other vertex.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example.
        Shortest path from vertex 0 to
        vertex 4 is (0 -> 2 -> 3 -> 4) with distance 4.8.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        shortest_dist = dijkstra_shortest_distance(graph, start_vertex, end_vertex)
        print(shortest_dist)

    .. code-block:: console

        4.8

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Shortest path from vertex 2 to
        vertex 0 is (2 -> 1 -> 0) with distance 2.7.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        end_vertex = 0

        shortest_dist = dijkstra_shortest_distance(graph, start_vertex, end_vertex)
        print(shortest_dist)

    .. code-block:: console

        2.7

    """
    _, distance_dict = dijkstra(
        graph,
        start,
        max_distance=max_distance,
        # stop_encounter=end, TODO: Optimizable ?
        weight_key=weight_key,
        _skip_check=_skip_check,
    )
    return distance_dict.get(end, -1.0)


def dijkstra_matrix(
    graph: Graph,
    *,
    weight_key: str = "weight",
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[List[float]]:
    r"""
    Compute the shortest path distance matrix for **all** pairs of vertices.

    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the Dijkstra. All vertices
        that are not reachable within this distance will be ignored.

    weight_key: str (default: ``'weight'``)
        The key-name of the weight to use in the graph dictionnary structure.
        If an edge does not have weight, default weight is ``1.0``.


    Returns
    -------
    List[List[float]]
        A 2D list representing the shortest path distance matrix, where the element
        at position (i, j) represents the shortest path distance from vertex i to
        vertex j. If a vertex is not reachable within the specified maximum distance,
        the distance will be ``-1.0``.


    Notes
    -----
    The function uses a Dijkstra approach to compute the shortest path distances, which
    is efficient for unweighted graphs.
    The time complexity is :math:`O(V(V + E))`, where :math:`V`
    is the number of vertices and :math:`E` is the number of edges in the graph.
    For a undirected graph, the distance matrix is symmetric, meaning that the distance from vertex
    :math:`A` to vertex :math:`B` is the same as the distance from vertex :math:`B` to vertex
    :math:`A` (i.e., :math:`\text{dist}(A, B) = \text{dist}(B, A)`), since the edges can be traversed
    in both directions. For a directed graph, the distance matrix is not necessarily symmetric, since the
    edges can only be traversed in one direction (i.e., :math:`\text{dist}(A, B)` may not be equal to
    :math:`\text{dist}(B, A)`).


    See Also
    --------
    :func:`pygraphs.dijkstra`
        Core implementation of Dijkstra.

    :func:`pygraphs.dijkstra_distances`
        Perform a breadth-first search (Dijkstra) to compute the shortest path distances
        from a starting vertex to all other vertices in the graph, where the distance
        is defined as the number of edges in the shortest path between the vertices.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distance matrix for all pairs of vertices in the graph.

    .. figure:: /_static/weighted_graph.png
        :align: center
        :width: 50%

        Disconnected and weighted graph with 7 vertices for Dijkstra example. Distance from vertex 0 to
        vertex 4 is 4.8 (0 -> 2 -> 3 -> 4). Thus ``dist[0, 4] = 4.8`` and ``dist[4, 0] = 4.8``
        for this undirected graph.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(0, 0.2), (1, 1.5), (3, 3.2)],
            [(2, 3.2), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            [(5, 2.3)]
        ]
        graph = Graph.from_adjacency(graph)

        adjacency_matrix = bfs_matrix(graph)
        print(f"adjacency_matrix (shape={len(adjacency_matrix)}x{len(adjacency_matrix[0])}):")
        print(adjacency_matrix)

    .. code-block:: console

        adjacency_matrix (shape=(7x7)):
        [[ 0.0  1.2  0.2  3.4  4.8 -1.0 -1.0]
         [ 1.2  0.0  1.4  4.6  6.0 -1.0 -1.0]
         [ 0.2  1.4  0.0  3.2  4.6 -1.0 -1.0]
         [ 3.4  4.6  3.2  0.0  1.4 -1.0 -1.0]
         [ 4.8  6.0  4.6  1.4  0.0 -1.0 -1.0]
         [-1.0 -1.0 -1.0 -1.0 -1.0  0.0  2.3]
         [-1.0 -1.0 -1.0 -1.0 -1.0  2.3  0.0]]


    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/weighted_graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for Dijkstra example. Shortest path from vertex 2 to
        vertex 0 is (2 -> 1 -> 0) with distance 2.7.

    .. code-block:: python
        :linenos:

        from pygraphs import dijkstra_k_disk, Graph

        graph = [
            [(1, 1.2), (2, 0.2)],
            [(0, 1.2), (2, 1.5)],
            [(1, 1.5), (3, 3.2)],
            [(2, 1.4), (4, 1.4)],
            [(3, 1.4)],
            [(6, 2.3)],
            []
        ]
        graph = Graph.from_adjacency(graph)

        adjacency_matrix = bfs_matrix(graph)
        print(f"adjacency_matrix (shape={len(adjacency_matrix)}x{len(adjacency_matrix[0])}):")
        print(adjacency_matrix)

    .. code-block:: console

        adjacency_matrix (shape=(7x7)):
        [[ 0.0  1.2  0.2  3.4  4.8 -1.0 -1.0]
         [ 1.2  0.0  1.4  4.6  6.0 -1.0 -1.0]
         [ 0.2  1.4  0.0  3.2  4.6 -1.0 -1.0]
         [ 1.6  2.8  1.4  0.0  1.4 -1.0 -1.0]
         [ 3.0  4.2  2.8  1.4  0.0 -1.0 -1.0]
         [-1.0 -1.0 -1.0 -1.0 -1.0  0.0  2.3]
         [-1.0 -1.0 -1.0 -1.0 -1.0 -1.0  0.0]]

    """
    if not isinstance(graph, Graph):
        raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")
    n_vertices = graph.n_vertices

    distance_matrix = []
    for i in range(n_vertices):
        distances = dijkstra_distances(
            graph,
            i,
            max_distance=max_distance,
            weight_key=weight_key,
            _skip_check=_skip_check or (i > 0),
        )
        distance_matrix.append(distances)
    return distance_matrix
