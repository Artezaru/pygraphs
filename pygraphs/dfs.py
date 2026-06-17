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

from typing import List, Optional, Tuple
from numbers import Integral

from .graph import Graph
from .scc import tarjan_components, kosaraju_components


def dfs(
    graph: Graph,
    start: Integral,
    *,
    stop_encounter: Optional[Integral] = None,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    [core function] Perform a depth-first search (DFS) traversal of a **unweighted** graph starting
    from a given vertex.

    The function returns the list of vertices visited in DFS order.

    .. warning::

        No tests are performed to check if the input graph is valid (e.g., if the graph
        contains self-loops, if the graph contains invalid vertex indices, ...).
        The behavior of the function is undefined if the input graph is not valid.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the DFS.

    stop_encounter : Optional[Integral], optional (default: ``None``)
        If provided, the BFS will stop as soon as this vertex is encountered.
        The provided vertex is included in the output.


    Returns
    -------
    order: List[int]
        List of vertices in the order they were visited by DFS.


    Notes
    -----

    - This is an **iterative DFS** implementation using an explicit stack.
    - Time complexity: O(V + E)
    - No guarantees are made about neighbor exploration order.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the component
    from a starting vertex (0).

    .. figure:: /_static/graph.png
        :align: center
        :width: 50%

        Disconnected graph with 7 vertices for DFS example. Component from vertex 0 is
        (0, 1, 2, 3, 4)

    .. code-block:: python
        :linenos:

        from pygraphs import dfs, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        ord = dfs(graph, start_vertex)
        print("Visited Order:", comp)

    .. code-block:: console

        Component: [0, 1, 2, 3, 4]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for DFS example. Componant of vertex 6 is
        only 6.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 6

        ord = dfs(graph, start_vertex)
        print("Visited Order:", ord)

    .. code-block:: console

        Component: [6]

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

    # -- DFS initialization --
    graph = graph._graph  # Dict[int, Dict[int, Dict[str, Any]]]
    visited = set()
    stack = [start]
    component = []

    while stack:
        u = stack.pop()

        if u in visited:
            continue

        visited.add(u)
        component.append(u)

        if stop_encounter is not None and u == stop_encounter:
            return component

        for v in graph[u]:
            if v not in visited:
                stack.append(v)

    return component


def dfs_reachable(
    graph: Graph,
    start: Integral,
    *,
    _skip_check: bool = False,
) -> List[int]:
    r"""
    Extract the vertices that are reachable from a starting vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the DFS.


    Returns
    -------
    List[int]
        A list of vertex indices representing the vertices that are reachable from the
        starting vertex in the graph.


    See Also
    --------
    :func:`pygraphs.dfs`
        Core implementation of DFS.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the vertices that are
    reachable from a starting vertex (0) in the graph.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for DFS example. Vertices 0, 1, 2, 3 and 4 are
       the only vertices that are reachable from vertex 0.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_reachable, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0

        reachable_vertices = dfs_reachable(
            graph, start_vertex
        )
        print(reachable_vertices)

    .. code-block:: console

        [0, 1, 2, 3, 4]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
       :align: center
       :width: 50%

       Directed graph with 7 vertices for DFS example. Vertices 5 is not
       reachable from vertex 6.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_reachable, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]

        graph = Graph.from_adjacency(graph)
        start_vertex = 6
        max_distance = None

        reachable_vertices = dfs_reachable(
            graph, start_vertex, max_distance=max_distance
        )
        print(reachable_vertices)

    .. code-block:: console

        [6]

    """
    order = dfs(graph, start, _skip_check=_skip_check)
    return order


def dfs_is_reachable(
    graph: Graph,
    start: Integral,
    end: Integral,
    *,
    _skip_check: bool = False,
) -> bool:
    r"""
    Check if a vertex is reachable from a starting vertex.


    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing the graph to be traversed.

    start: Integral
        The starting vertex index for the DFS.

    end: Integral
        The ending vertex index for the DFS.


    Returns
    -------
    bool
        If the ending vertex is reachable from starting vertex.


    See Also
    --------
    :func:`pygraphs.dfs`
        Core implementation of DFS.

    :func:`pygraphs.dfs_reachable`
        Perform a depth-first search (DFS) to extract the vertices that are reachable from a
        starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and compute the shortest path
    distances from a starting vertex (0) to all other vertices in the graph.

    .. figure:: /_static/graph.png
       :align: center
       :width: 50%

       Disconnected graph with 7 vertices for DFS example. Vertex 4 is reachable from
       vertex 0.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_is_reachable, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)
        start_vertex = 0
        end_vertex = 4

        is_reach = dfs_is_reachable(graph, start_vertex, end_vertex)
        print(is_reach)

    .. code-block:: console

        True

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for DFS example. Vertex 5 is not reachable
        from vertex 6.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_is_reachable, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)
        start_vertex = 6
        end_vertex = 5

        is_reach = dfs_is_reachable(graph, start_vertex, end_vertex)
        print(is_reach)

    .. code-block:: console

        False

    """
    order = dfs(graph, start, stop_encounter=end, _skip_check=_skip_check)
    return end in order


def dfs_components(
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
    :func:`pygraphs.dfs`
        Core implementation of DFS.

    :func:`pygraphs.dfs_reachable`
        Perform a breadth-first search (DFS) to extract the vertices that are reachable from a
        starting vertex in the graph.


    Examples
    --------
    Create a simple disconnected graph of 7 vertices and check if a vertex is reachable
    from an other.

    .. figure:: /_static/graph.png
        :align: center
        :width: 50%

        Disconnected graph with 7 vertices for DFS example. The graph has 2 connected components:
        {0, 1, 2, 3, 4} and {5, 6}.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_components, Graph

        graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
        graph = Graph.from_adjacency(graph)

        components = dfs_components(graph)
        print(components)

    .. code-block:: console

        [[0, 1, 2, 3, 4], [5, 6]]

    This method can be applied for **directed** graphs as well,
    where the adjacency list represents the outgoing neighbors of each vertex.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices for DFS example. The graph has 2 connected components:
        {0, 1, 2, 3, 4}, {5,6} using ``strongly_connected=False`` and 4 connected components:
        {0, 1, 2}, {3, 4}, {5} and {6} using ``strongly_connected=True``.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_components, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = dfs_components(graph, strongly_connected=False)
        print(components)

    .. code-block:: console

        [[0, 1, 2, 3, 4], [5, 6]]

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_components, Graph

        graph = [[1, 2], [0, 2], [1, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = dfs_components(graph, strongly_connected=True)
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
                component = dfs_reachable(graph, vertex, _skip_check=True)
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
