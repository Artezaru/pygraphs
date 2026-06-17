"""
pygraphs - Python graphs library to perform BFS, DFS, Dijkstra, and more.
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
from numbers import Integral
from collections import deque

from .graph import Graph
from .scc import tarjan_components, kosaraju_components


def bfs(
    graph: Graph,
    start: Integral,
    *,
    max_distance: Optional[Integral] = None,
    stop_encounter: Optional[Integral] = None,
    _skip_check: bool = False,
) -> Tuple[Dict[int, int], Dict[int, int]]:
    r"""
    [core function] Perform a breadth-first search (BFS) to compute the shortest path distances from
    a starting vertex to all other vertices in a **unweighted** graph, and to keep track
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
        The starting vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.

    stop_encounter : Optional[Integral], optional (default: ``None``)
        If provided, the BFS will stop as soon as this vertex is encountered.
        The provided vertex is included in the output.


    Returns
    -------
    parents: Dict[int, int]
        A dictionary mapping each visited vertex index to its parent vertex index in the BFS tree.
        The starting vertex will have a parent of None.

    distances: Dict[int, int]
        A dictionary mapping each visited vertex index to its shortest path distance from the
        starting vertex. The starting vertex will have a distance of 0.


    Notes
    -----
    The function uses a breadth-first search (BFS) algorithm to compute shortest path
    distances in an unweighted graph.

    BFS explores the graph level by level starting from the source vertex.
    It first visits all vertices at distance 1, then all vertices at distance 2, and so on.
    This guarantees that the first time a vertex is visited, the path used is the shortest (in number of edges).

    The algorithm maintains a queue of vertices to explore and a dictionary of distances
    initialized with the source vertex at distance 0. Each time a vertex is processed,
    all of its unvisited neighbors are assigned a distance equal to the current
    vertex distance plus one and are added to the queue.

    This process continues until all reachable vertices are visited or until an optional
    stopping condition is met.

    The time complexity is :math:`O(V + E)`, where :math:`V` is the number of vertices
    and :math:`E` is the number of edges in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distances from a starting vertex (0) to all other vertices in the graph.

    .. figure:: /_static/graph.png
        :align: center
        :width: 50%

        Disconnected graph with 7 vertices for BFS example. Distance from vertex 0 to
        vertex 4 is 3 (0 -> 2 -> 3 -> 4).

    .. code-block:: python
        :linenos:

        from pygraphs import bfs, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        parent, distance = bfs(graph, start_vertex)
        print("Parent:", parent)
        print("Distance:", distance)

    .. code-block:: console

        Parent: {0: None, 1: 0, 2: 0, 3: 2, 4: 3}
        Distance: {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Distance from vertex 2 to
        vertex 0 is 2 (2 -> 1 -> 0).

    .. code-block:: python
        :linenos:

        from pygraphs import bfs, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2

        parent, distance = bfs(graph, start_vertex)
        print("Parent:", parent)
        print("Distance:", distance)

    .. code-block:: console

        Parent: {2: None, 1: 2, 3: 2, 0: 1, 4: 3}
        Distance: {2: 0, 1: 1, 3: 1, 0: 2, 4: 2}

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

        if max_distance is not None and (not isinstance(max_distance, Integral)):
            raise TypeError(
                f"max_distance must be an integer or None. Got {type(max_distance)}."
            )
        if max_distance is not None and max_distance < 0:
            raise ValueError(
                f"max_distance must be a non-negative integer or None."
                f" Got {max_distance}."
            )
        if max_distance is not None:
            max_distance = int(max_distance)

        if stop_encounter is not None and (not isinstance(stop_encounter, Integral)):
            raise TypeError(
                f"stop_encounter must be an integer or None. Got {type(stop_encounter)}."
            )
        if stop_encounter is not None and (
            stop_encounter < 0 or stop_encounter >= graph.n_vertices
        ):
            raise ValueError(
                f"stop_encounter must be an integer between 0 and n_vertices-1 or None."
                f" Got {stop_encounter}."
            )
        if stop_encounter is not None:
            stop_encounter = int(stop_encounter)

    # -- BFS initialization --
    graph = graph._graph  # Dict[int, Dict[int, Dict[str, Any]]]
    parents = {start: None}
    distances = {start: 0}
    queue = deque([start])

    # -- BFS loop --
    while queue:
        node = queue.popleft()
        d = distances[node]

        for nbr in graph[node].keys():
            if nbr not in distances:
                nd = d + 1

                # -- Skip node farther than max_distance --
                if max_distance is not None and nd > max_distance:
                    continue

                # -- Stop BFS if stop_encounter is reached --
                if stop_encounter is not None and nbr == stop_encounter:
                    parents[nbr] = node
                    distances[nbr] = nd
                    return parents, distances

                parents[nbr] = node
                distances[nbr] = nd
                queue.append(nbr)

    return parents, distances


def bfs_distances(
    graph: Graph,
    start: Integral,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Compute shortest path distances from a source vertex to **all** reachable vertices
    using BFS.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    List[int]
        A list of integers representing the shortest path distances from the starting
        vertex to all other vertices in the graph.
        The length of the output list is equal to the number of vertices in the graph.
        Unreachable vertices have distance of ``-1``.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_matrix`
        Compute the shortest path distance matrix for all pairs of vertices in the graph
        using breadth-first search (BFS).


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distances from a starting vertex (0) to all other vertices in the graph.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Distance from vertex 0 to
       vertex 4 is 3 (0 -> 2 -> 3 -> 4).


    .. code-block:: python
        :linenos:

        from pygraphs import bfs_distances, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        distances = bfs_distances(graph, start_vertex)
        print(distances)

    .. code-block:: console

        [0, 1, 1, 2, 3, -1, -1]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Distance from vertex 2 to
        vertex 0 is 2 (2 -> 1 -> 0).

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_distances, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2

        distances = bfs_distances(graph, start_vertex)
        print(distances)

    .. code-block:: console

        [2, 1, 0, 1, 2, -1, -1]

    """
    _, distance_dict = bfs(
        graph,
        start,
        max_distance=max_distance,
        _skip_check=_skip_check,
    )
    n_vertices = graph.n_vertices
    return [distance_dict.get(i, -1) for i in range(n_vertices)]


def bfs_k_annulus(
    graph: Graph,
    start: Integral,
    inner_distance: Optional[Integral],
    outer_distance: Optional[Integral],
    *,
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
        The starting vertex index for the BFS.

    inner_distance : Optional[Integral]
        The minimum distance :math:`k_1` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are at least this distance from the vertex.
        If None, there is no minimum distance and all vertices that are at
        least 0 distance from the vertex are included.

    outer_distance : Optional[Integral]
        The maximum distance :math:`k_2` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are at most this distance from the vertex.
        If None, there is no maximum distance and all vertices that are reachable
        from the starting vertex are included.


    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices in the adjacency annulus
        of the starting vertex in the graph (i.e., the set of vertices that are between
        inner_distance and outer_distance from the starting vertex).


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_k_disk`
        Call this function with ``inner_distance = 0`` and ``outer_distance = k`` to extract the
        vertices in a adjacency disk of a starting vertex in the graph.

    :func:`pygraphs.bfs_k_ring`
        Call this function with ``inner_distance = k`` and ``outer_distance = k`` to extract the
        vertices in a adjacency ring of a starting vertex in the graph.

    :func:`pygraphs.bfs_distances`
        Perform a breadth-first search (BFS) to compute the shortest path distances
        from a starting vertex to all other vertices in the graph, where the distance
        is defined as the number of edges in the shortest path between the vertices.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and extract the vertices within
    distance range.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Vertices 1, 2 and 3 are the only
       vertices in the neighborhood of vertex 0 for inner_distance = 1 and outer_distance = 2.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_annulus, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        start_vertex = 0
        inner_distance = 1
        outer_distance = 2

        neighborhood = bfs_k_annulus(
            graph, start_vertex, inner_distance, outer_distance
        )
        print(neighborhood)

    .. code-block:: console

        [1, 2, 3]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Vertices 1 and 3 are the only
        vertices in the neighborhood of vertex 2 for inner_distance = 1 and outer_distance = 1.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_annulus, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        start_vertex = 2
        inner_distance = 1
        outer_distance = 1

        neighborhood = bfs_k_annulus(
            graph, start_vertex, inner_distance, outer_distance
        )
        print(neighborhood)

    .. code-block:: console

        [1, 3]

    """
    if inner_distance is not None and not isinstance(inner_distance, Integral):
        raise TypeError(
            f"inner_distance must be an integer. Got {type(inner_distance)}."
        )
    if inner_distance is not None and inner_distance < 0:
        raise ValueError(
            f"inner_distance must be a non-negative integer." f" Got {inner_distance}."
        )
    if inner_distance is not None:
        inner_distance = int(inner_distance)
    else:
        inner_distance = 0

    if outer_distance is not None and not isinstance(outer_distance, Integral):
        raise TypeError(
            f"outer_distance must be an integer. Got {type(outer_distance)}."
        )
    if outer_distance is not None and outer_distance < 0:
        raise ValueError(
            f"outer_distance must be a non-negative integer." f" Got {outer_distance}."
        )
    if outer_distance is not None:
        outer_distance_bfs = int(outer_distance)
        outer_distance = int(outer_distance)
    else:
        outer_distance_bfs = None
        outer_distance = float("inf")

    if inner_distance > outer_distance:
        return []

    _, distance_dict = bfs(
        graph,
        start,
        max_distance=outer_distance_bfs,
        _skip_check=_skip_check,
    )
    return [
        v for v, d in distance_dict.items() if inner_distance <= d <= outer_distance
    ]


def bfs_k_disk(
    graph: Graph,
    start: Integral,
    distance: Integral,
    *,
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
        The starting vertex index for the BFS.

    distance : Integral
        The adjacency radius :math:`k` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are within this distance from the vertex.

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
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_k_annulus`
        Call this function with ``inner_distance = 0`` and ``outer_distance = k`` to extract the
        vertices in a adjacency annulus of a starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and extract the vertices within
    distance range.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Vertices 0, 1, 2 and 3 are
       the only vertices in the neighborhood of vertex 0 for distance = 2.


    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_disk, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        distance = 2

        neighborhood = bfs_k_disk(
            graph, start_vertex, distance, self_neighborhood=True
        )
        print(neighborhood)


    .. code-block:: console

        [0, 1, 2, 3]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
       :align: center
       :width: 50%

       Directed graph with 7 vertices for BFS example. Vertices 1, 2 and 3 are the only
       vertices in the neighborhood of vertex 2 for distance = 1.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_disk, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        distance = 1

        neighborhood = bfs_k_disk(
            graph, start_vertex, distance, self_neighborhood=False
        )
        print(neighborhood)

    .. code-block:: console

        [1, 3]

    """
    if not isinstance(self_neighborhood, bool):
        raise TypeError(
            f"self_neighborhood must be a boolean. Got {type(self_neighborhood)}."
        )

    if self_neighborhood:
        inner_distance = 0
    else:
        inner_distance = 1

    return bfs_k_annulus(
        graph,
        start,
        inner_distance,
        distance,
        _skip_check=_skip_check,
    )


def bfs_k_ring(
    graph: Graph,
    start: Integral,
    distance: Integral,
    *,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Return all vertices with distance equal to :math:`k`
    (ie :math:`\{v \in V | \text{dist}(i, v) = k\}`) where :math:`k` is
    the specified distance.


    Parameters
    ----------
    graph : Graph
        An instance of the Graph class representing the graph to be traversed.

    start : Integral
        The starting vertex index for the BFS.

    distance : Integral
        The adjacency radius :math:`k` for the neighborhood of the starting vertex,
        where the neighborhood includes all vertices that are at this distance from the
        starting vertex.


    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices in the adjacency ring
        of the starting vertex at the specified distance. If no vertices are found
        at the specified distance, an empty list is returned.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_k_annulus`
        Call this function with ``inner_distance = k`` and ``outer_distance = k`` to extract the
        vertices in a adjacency annulus of a starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and extract the vertices within
    distance range.

    .. figure:: /_static/graph.png
        :align: center
        :width: 50%

        Disconnected graph with 7 vertices for BFS example. Vertices 1 and 2 are the only
        vertices in the neighborhood of vertex 0 for distance = 1.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_ring, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        distance = 1

        neighborhood = bfs_k_ring(
            graph, start_vertex, distance
        )
        print(neighborhood)

    .. code-block:: console

        [1, 2]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Vertices 1 and 3 are the only
        vertices in the neighborhood of vertex 2 for distance = 1.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_k_ring, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        distance = 1

        neighborhood = bfs_k_ring(
            graph, start_vertex, distance
        )
        print(neighborhood)

    .. code-block:: console

        [1, 3]

    """
    return bfs_k_annulus(graph, start, distance, distance, _skip_check=_skip_check)


def bfs_shortest_path(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Compute the shortest path from a starting vertex to an ending vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the BFS.

    end: Integral
        The ending vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    List[int]
        A list of vertex indices representing the shortest path from the starting vertex
        to the ending vertex in the graph. If there is no path from the starting vertex
        to the ending vertex, an empty list is returned.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    from a starting vertex (0) to an other vertex.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Shortest path from vertex 0 to
       vertex 4 is (0 -> 2 -> 3 -> 4).

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_shortest_path, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        shortest_path = bfs_shortest_path(graph, start_vertex, end_vertex)
        print(shortest_path)

    .. code-block:: console

        [0, 2, 3, 4]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Shortest path from vertex 2 to
        vertex 0 is (2 -> 1 -> 0).

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_shortest_path, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        end_vertex = 0

        shortest_path = bfs_shortest_path(graph, start_vertex, end_vertex)
        print(shortest_path)

    .. code-block:: console

        [2, 1, 0]

    """
    parent, distance_dict = bfs(
        graph,
        start,
        max_distance=max_distance,
        stop_encounter=end,
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


def bfs_shortest_distance(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> int:
    r"""
    Compute the shortest distance from a starting
    vertex to an ending vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the BFS.

    end: Integral
        The ending vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    int
        The distance from starting vertex to ending vertex. Or ``-1`` if not reachable.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_distances`
        Perform a breadth-first search (BFS) to compute the shortest path distances
        from a starting vertex to all other vertices in the graph, where the distance
        is defined as the number of edges in the shortest path between the vertices.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest distance
    from a starting vertex (0) to an other vertex.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Shortest path from vertex 0 to
       vertex 4 is (0 -> 2 -> 3 -> 4) with distance 3.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_shortest_distance, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        shortest_dist = bfs_shortest_distance(graph, start_vertex, end_vertex)
        print(shortest_dist)

    .. code-block:: console

        3

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Shortest path from vertex 2 to
        vertex 0 is (2 -> 1 -> 0) with distance 2.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_shortest_distance, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 2
        end_vertex = 0

        shortest_dist = bfs_shortest_distance(graph, start_vertex, end_vertex)
        print(shortest_dist)

    .. code-block:: console

        2

    """
    _, distance_dict = bfs(
        graph,
        start,
        max_distance=max_distance,
        stop_encounter=end,
        _skip_check=_skip_check,
    )
    return distance_dict.get(end, -1)


def bfs_is_reachable(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> bool:
    r"""
    Check if a vertex is reachable from a starting vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the BFS.

    end: Integral
        The ending vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    bool
        If the ending vertex is reachable from starting vertex within the given distance.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_reachable`
        Perform a breadth-first search (BFS) to extract the vertices that are reachable from a
        starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and check if a vertex is reachable
    from an other.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Vertex 4 is reachable from
       vertex 0.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_is_reachable, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        is_reach = bfs_is_reachable(graph, start_vertex, end_vertex)
        print(is_reach)

    .. code-block:: console

        True

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. Vertex 5 is not reachable
        from vertex 6.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_is_reachable, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 6
        end_vertex = 5

        is_reach = bfs_is_reachable(graph, start_vertex, end_vertex)
        print(is_reach)

    .. code-block:: console

        False

    """
    dist = bfs_shortest_distance(
        graph, start, end, max_distance=max_distance, _skip_check=_skip_check
    )
    return dist != -1


def bfs_matrix(
    graph: Graph,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[List[int]]:
    r"""
    Compute the shortest path distance matrix for **all** pairs of vertices.

    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    List[List[int]]
        A 2D list representing the shortest path distance matrix, where the element
        at position (i, j) represents the shortest path distance from vertex i to
        vertex j. If a vertex is not reachable within the specified maximum distance,
        the distance will be ``-1``.


    Notes
    -----
    The function uses a BFS approach to compute the shortest path distances, which
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
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_distances`
        Perform a breadth-first search (BFS) to compute the shortest path distances
        from a starting vertex to all other vertices in the graph, where the distance
        is defined as the number of edges in the shortest path between the vertices.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distance matrix for all pairs of vertices in the graph.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for bfs matrix example. Distance from vertex 0 to
       vertex 4 is 3 (0 -> 2 -> 3 -> 4). Thus ``dist[0, 4] = 3`` and ``dist[4, 0] = 3``
       for this undirected graph.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_matrix, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)

        adjacency_matrix = bfs_matrix(graph)
        print(f"adjacency_matrix (shape={len(adjacency_matrix)}x{len(adjacency_matrix[0])}):")
        print(adjacency_matrix)

    .. code-block:: console

        adjacency_matrix (shape=(7x7)):
        [[ 0  1  1  2  3 -1 -1]
         [ 1  0  1  2  3 -1 -1]
         [ 1  1  0  1  2 -1 -1]
         [ 2  2  1  0  1 -1 -1]
         [ 3  3  2  1  0 -1 -1]
         [-1 -1 -1 -1 -1  0  1]
         [-1 -1 -1 -1 -1  1  0]]

    .. note::

        For undirected graphs (``graph.is_directed() == False``), the distance matrix
        is symmetric.


    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
       :align: center
       :width: 50%

       Directed graph with 7 vertices for bfs matrix example. Distance from vertex 2 to
       vertex 0 is 2 (2 -> 1 -> 0) and distance from vertex 0 to vertex 2 is 1 (0 -> 2).

    .. code-block:: python
        :linenos:

        from pygraphs import compute_adjacency_matrix, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        adjacency_matrix = bfs_matrix(graph)
        print(f"adjacency_matrix (shape={len(adjacency_matrix)}x{len(adjacency_matrix[0])}):")
        print(adjacency_matrix)

    .. code-block:: console

        adjacency_matrix (shape=(7x7)):
        [[ 0  1  1  2  3 -1 -1]
         [ 1  0  1  2  3 -1 -1]
         [ 2  1  0  1  2 -1 -1]
         [ 3  2  1  0  1 -1 -1]
         [ 4  3  2  1  0 -1 -1]
         [-1 -1 -1 -1 -1  0  1]
         [-1 -1 -1 -1 -1 -1 0]]


    """
    if not isinstance(graph, Graph):
        raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")
    n_vertices = graph.n_vertices

    distance_matrix = []
    for i in range(n_vertices):
        distances = bfs_distances(
            graph, i, max_distance=max_distance, _skip_check=_skip_check or (i > 0)
        )
        distance_matrix.append(distances)
    return distance_matrix


def bfs_reachable(
    graph: Graph,
    start: Integral,
    *,
    max_distance: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Extract the vertices that are reachable from a starting vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the BFS.

    max_distance : Optional[Integral], optional (default: ``None``)
        The maximum distance to search for in the BFS. All vertices
        that are not reachable within this distance will be ignored.


    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices that are reachable from the
        starting vertex in the graph.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the vertices that are
    reachable from a starting vertex (0) in the graph.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for BFS example. Vertices 0, 1, 2, 3 and 4 are
       the only vertices that are reachable from vertex 0.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_reachable, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        max_distance = None

        reachable_vertices = bfs_reachable(
            graph, start_vertex, max_distance=max_distance
        )
        print(reachable_vertices)

    .. code-block:: console

        [0, 1, 2, 3, 4]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
       :align: center
       :width: 50%

       Directed graph with 7 vertices for BFS example. Vertices 5 is not
       reachable from vertex 6.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_reachable, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]

        graph = Graph.from_adjacency(graph)
        start_vertex = 6
        max_distance = None

        reachable_vertices = bfs_reachable(
            graph, start_vertex, max_distance=max_distance
        )
        print(reachable_vertices)

    .. code-block:: console

        [6]

    """
    _, distance_dict = bfs(
        graph, start, max_distance=max_distance, _skip_check=_skip_check
    )
    return list(distance_dict.keys())


def bfs_components(
    graph: Graph,
    *,
    strongly_connected: bool = False,
    scc_mode: str = "tarjan",
    _skip_check: bool = False,
) -> List[List[int]]:
    r"""
    Extract the connected components (or strongly connected components
    if ``strongly_connected=True``) of the graph.

    .. note::

        Vertices A and B are in the same component if :

        - connected component: there is a path from vertex A to vertex B **OR** from vertex B to vertex A.
        - strongly connected component : there is a path from vertex A to vertex B **AND** from vertex B to vertex A.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    strongly_connected: bool (default: ``False``)
        Compute the strongly connected components instead.

    scc_mode: str (default: ``'tarjan'``)
        The efficient method to compute strongly connected components.
        Available options are ``'tarjan'`` or ``'kosaraju'``.


    Returns
    -------
    List[List[int]]
        A list of lists, where each inner list represents a connected component of the graph.
        Each connected component is a list of vertex indices that are reachable from each other.
        If the graph is empty, an empty list is returned.


    Notes
    -----
    For ``strongly_connected=False``, considering the **undirected** graph associated
    with the provided, a BFS is performed starting
    from an unvisited vertex, and all vertices that are reachable from that vertex
    are added to the same component.

    For ``strongly_connected=True``, call Tarjan or Kosaraju algorithm.


    See Also
    --------
    :func:`pygraphs.bfs`
        Core implementation of BFS.

    :func:`pygraphs.bfs_reachable`
        Perform a breadth-first search (BFS) to extract the vertices that are reachable from a
        starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the
    connected components of the graph.

    .. figure:: /_static/graph.png
        :align: center
        :width: 50%

        Disconnected graph with 7 vertices for BFS example. The graph has 2 connected components:
        {0, 1, 2, 3, 4} and {5, 6}.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_components, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)

        components = bfs_components(graph)
        print(components)

    .. code-block:: console

        [[0, 1, 2, 3, 4], [5, 6]]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for BFS example. The graph has 2 connected components:
        {0, 1, 2, 3, 4}, {5,6} using ``strongly_connected=False`` and 4 connected components:
        {0, 1, 2}, {3, 4}, {5} and {6} using ``strongly_connected=True``.

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_components, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = bfs_components(graph, strongly_connected=False)
        print(components)

    .. code-block:: console

        [[0, 1, 2, 3, 4], [5, 6]]

    .. code-block:: python
        :linenos:

        from pygraphs import bfs_components, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = bfs_components(graph, strongly_connected=True)
        print(components)

    .. code-block:: console

        [[0, 1, 2], [3, 4], [5], [6]]

    """
    if not _skip_check:
        if not isinstance(graph, Graph):
            raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")

    n_vertices = graph.n_vertices

    if not isinstance(strongly_connected, bool):
        raise TypeError(
            f"strongly_connected must be a boolean. Got {type(strongly_connected)}."
        )

    if not strongly_connected:
        graph = graph.to_clean().to_undirected()

        # For undirect graph, a unvisited vertex is in an other component !
        components = []
        visited = set()

        for i, vertex in enumerate(range(n_vertices)):
            if vertex not in visited:
                component = bfs_reachable(graph, vertex, _skip_check=True)
                component_set = set(component)
                visited.update(component_set)
                components.append(component)

        return components

    else:
        if scc_mode not in ["tarjan", "kosaraju"]:
            raise ValueError(
                f"scc_mode must be 'tarjan' or 'kosaraju'. Got {scc_mode}."
            )

        if scc_mode == "tarjan":
            return tarjan_components(graph, _skip_check=True)

        elif scc_mode == "kosaraju":
            return kosaraju_components(graph, _skip_check=True)
