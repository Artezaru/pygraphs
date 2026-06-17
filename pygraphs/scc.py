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

from typing import List

from .graph import Graph


def kosaraju_components(graph: Graph, *, _skip_check: bool = False) -> List[List[int]]:
    r"""
    Compute the **strongly connected components (SCC)** of a directed graph using the
    Kosaraju algorithm (based on DFS).

    A strongly connected component is a maximal set of vertices such that every vertex is reachable
    from every other vertex in both directions.

    In other words, for any vertices u and v in the same component:
    there exists a path from u to v **and** a path from v to u.

    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing a **directed** graph on which
        strongly connected components will be computed.


    Returns
    -------
    List[List[int]]
        A list of strongly connected components.
        Each component is represented as a list of vertex indices.
        The order of components is not guaranteed.

        If the graph is empty, an empty list is returned.


    Notes
    -----
    Kosaraju's algorithm computes strongly connected components using two DFS traversals.

    It proceeds in three main steps:

    - a first DFS to compute the vertices in order of finishing time,
    - reversal of all edges in the graph,
    - a second DFS on the reversed graph following the reverse finishing order.

    During the second pass, each DFS tree identifies a strongly connected component.

    A strongly connected component is a maximal set of vertices such that every vertex
    is reachable from every other vertex in both directions.

    In other words, for any vertices u and v in the same component:
    there exists a path from u to v **and** a path from v to u.

    Kosaraju's algorithm maintains:

    - a list of vertices ordered by decreasing finishing time from the first DFS,
    - a reversed version of the input graph,
    - a visited set to avoid revisiting nodes during the second DFS.

    Each time a new DFS is started in the second pass, all reachable vertices in the reversed graph
    form a complete strongly connected component.

    Complexity:

    - Time complexity: :math:`O(V + E)`
    - Space complexity: :math:`O(V)`

    Unlike Tarjan's algorithm, Kosaraju requires building the reversed graph
    and performing two separate DFS traversals, but is often simpler to implement and reason about.


    See Also
    --------
    :func:`pygraphs.dfs`
        Core depth-first search traversal.


    Examples
    --------
    Create a simple directed graph of 7 vertices and compute its strongly connected components.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices. Strongly connected components are:
        {0, 1, 2}, {3, 4}, {5}, {6}.

    .. code-block:: python
        :linenos:

        from pygraphs import dfs_kosaraju, Graph

        graph = [[1, 2], [0, 2], [1, 0, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = dfs_kosaraju(graph)
        print(components)

    .. code-block:: console

        [[0, 1, 2], [3, 4], [5], [6]]

    """
    if not _skip_check:
        if not isinstance(graph, Graph):
            raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")

    n_vertices = graph.n_vertices

    visited = set()
    order = []

    graph_raw = graph._graph

    # 1. DFS to ending order
    def dfs_order(u: int):
        stack = [u]

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            for v in graph_raw[node]:
                if v not in visited:
                    stack.append(v)

            order.append(node)

    for v in range(n_vertices):
        if v not in visited:
            dfs_order(v)

    # 2. reversing graph
    reversed_graph = {i: {} for i in range(n_vertices)}

    for u in graph_raw:
        for v in graph_raw[u]:
            reversed_graph[v][u] = {}

    # 3. DFS on inversed graph
    visited.clear()
    components = []

    def dfs_component(u: int, comp: list[int]):
        stack = [u]

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)
            comp.append(node)

            for v in reversed_graph[node]:
                if v not in visited:
                    stack.append(v)

    for v in reversed(order[::-1]):  # ordre inverse de fin
        if v not in visited:
            comp = []
            dfs_component(v, comp)
            components.append(comp)

    return components


def tarjan_components(graph: Graph, *, _skip_check: bool = False) -> List[List[int]]:
    r"""
    Compute the **strongly connected components (SCC)** of a directed graph using
    Tarjan's algorithm.

    A strongly connected component is a maximal set of vertices such that every vertex
    is reachable from every other vertex in both directions.

    In other words, for any vertices u and v in the same component:
    there exists a path from u to v **and** a path from v to u.

    Parameters
    ----------
    graph: Graph
        An instance of the Graph class representing a **directed graph** on which
        strongly connected components will be computed.

    _skip_check: bool, optional (default: ``False``)
        If True, skip input validation checks for performance reasons.

    Returns
    -------
    List[List[int]]
        A list of strongly connected components.
        Each component is represented as a list of vertex indices.

        The order of components is not guaranteed.

        If the graph is empty, an empty list is returned.

    Notes
    -----
    Tarjan's algorithm computes strongly connected components in a single DFS traversal.

    It maintains:

    - an *index* counter assigning a unique discovery time to each node,
    - a *low-link value* representing the smallest index reachable from a node,
    - a stack of active nodes currently in the DFS recursion tree.

    A node is identified as the root of a strongly connected component when:
    `lowlink[node] == index[node]`.

    At this point, all nodes on the stack up to that node form a complete SCC.

    Complexity:

    - Time complexity: :math:`O(V + E)`
    - Space complexity: :math:`O(V)`

    Unlike Kosaraju's algorithm, Tarjan does not require reversing the graph
    or performing multiple DFS passes.

    See Also
    --------
    :func:`pygraphs.dfs`
        Core depth-first search traversal.

    :func:`pygraphs.kosaraju_components`
        Alternative SCC algorithm based on two DFS passes.

    Examples
    --------
    Create a simple directed graph of 7 vertices and compute its strongly connected components.

    .. figure:: /_static/graph_directed.png
        :align: center
        :width: 50%

        Directed graph with 7 vertices. Strongly connected components are:
        {0, 1, 2}, {3, 4}, {5}, {6}.

    .. code-block:: python
        :linenos:

        from pygraphs import tarjan_components, Graph

        graph = [[1, 2], [0, 2], [1, 0, 3], [4], [3], [6], []]
        graph = Graph.from_adjacency(graph)

        components = tarjan_components(graph)
        print(components)

    .. code-block:: console

        [[0, 1, 2], [3, 4], [5], [6]]

    """
    if not _skip_check:
        if not isinstance(graph, Graph):
            raise TypeError(f"graph must be an instance of Graph. Got {type(graph)}.")

    n_vertices = graph.n_vertices
    graph_raw = graph._graph

    index = 0
    stack = []
    on_stack = set()

    indices = {}
    lowlink = {}
    components: List[List[int]] = []

    def dfs(v: int) -> None:
        nonlocal index

        indices[v] = index
        lowlink[v] = index
        index += 1

        stack.append(v)
        on_stack.add(v)

        for w in graph_raw[v]:
            if w not in indices:
                dfs(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        # If v is a root node, pop the stack and build an SCC
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            components.append(comp)

    for v in range(n_vertices):
        if v not in indices:
            dfs(v)

    return components
