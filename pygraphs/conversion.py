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

from typing import Optional
from numbers import Integral

from .types import (
    Edges,
    AdjacencyList,
    GraphRepresentation,
)
from .exeptions import (
    assert_valid_graph,
    assert_valid_edges,
    assert_valid_adjacency_list,
)


def adjacency_list_to_graph(
    adjacency: AdjacencyList, *, weight_key: str = "weight", skip_validation=False
) -> GraphRepresentation:
    r"""
    Convert a graph represented as an adjacency list (``AdjacencyList``) to a graph
    represented as a dictionary (``GraphRepresentation``).

    .. include:: /_static/rstdoc/adjacency_list_representation.rst

    .. include:: /_static/rstdoc/graph_representation.rst

    Parameters
    ----------
    adjacency : AdjacencyList
        The adjacency list to convert into graph representation.

    weight_key : str, optional (default: ``'weight'``)
        The key to use for storing edge weights in the graph
        representation when the adjacency list is weighted.

    Returns
    -------
    graph : GraphRepresentation
        The graph represented as a dictionary.

    """
    if not skip_validation:
        assert_valid_adjacency_list(adjacency)
    if not isinstance(weight_key, str):
        raise ValueError("The 'weight_key' parameter must be a string.")

    graph = {}
    for u, neighbors in enumerate(adjacency):
        graph[u] = {}
        for neighbor in neighbors:
            if isinstance(neighbor, Integral):
                v = neighbor
                graph[u][int(v)] = {}
            else:
                v, w = neighbor
                if isinstance(w, dict):
                    graph[u][int(v)] = w
                else:
                    graph[u][int(v)] = {weight_key: float(w)}

    return graph


def edges_list_to_graph(
    edges: Edges,
    n_vertices: Integral,
    *,
    weight_key: str = "weight",
    skip_validation=False
) -> GraphRepresentation:
    r"""
    Convert a graph represented as an edge list (``Edges``) to a graph represented
    as a dictionary (``GraphRepresentation``).

    .. include:: /_static/rstdoc/edges_representation.rst

    .. include:: /_static/rstdoc/graph_representation.rst

    Parameters
    ----------
    edges : Edges
        The edge list to convert into graph representation.

    n_vertices : Integral
        The number of vertices in the graph.

    weight_key : str, optional (default: ``'weight'``)
        The key to use for storing edge weights in the graph
        representation when the edge list is weighted.

    Returns
    -------
    graph : GraphRepresentation
        The graph represented as a dictionary.

    """
    if not skip_validation:
        assert_valid_edges(edges, n_vertices)
    if not isinstance(weight_key, str):
        raise ValueError("The 'weight_key' parameter must be a string.")

    graph = {u: {} for u in range(n_vertices)}
    for edge in edges:
        if len(edge) == 2:
            u, v = edge
            graph[int(u)][int(v)] = {}
        else:
            u, v, w = edge
            if isinstance(w, dict):
                graph[int(u)][int(v)] = w
            else:
                graph[int(u)][int(v)] = {weight_key: float(w)}

    return graph


def graph_to_adjacency_list(
    graph: GraphRepresentation,
    *,
    weighted: bool = False,
    weight_key: Optional[str] = "weight",
    dicted: bool = True,
    skip_validation=False
) -> AdjacencyList:
    r"""
    Convert a graph represented as a dictionary (``GraphRepresentation``) to a graph
    represented as an adjacency list (``AdjacencyList``).

    .. include:: /_static/rstdoc/adjacency_list_representation.rst

    .. include:: /_static/rstdoc/graph_representation.rst


    Parameters
    ----------
    graph : GraphRepresentation
        The graph represented as a dictionary.

    weighted : bool, optional (default: ``False``)
        Whether to represent the graph as ``List[List[Tuple[Integral, Real]]]``.

    weight_key : Optional[str], optional (default: ``'weight'``)
        The key to use for accessing the weight of an edge in the graph representation.
        Ignored if ``weighted`` is False.

    dicted : bool, optional (default: ``False``)
        Whether to represent the graph as ``List[List[Tuple[Integral, Dict[str, Any]]]]``.


    Returns
    -------
    adjacency_list : AdjacencyList
        The graph represented as an adjacency list.

    """
    if not skip_validation:
        assert_valid_graph(graph)
    if not isinstance(weighted, bool):
        raise ValueError("The 'weighted' parameter must be a boolean.")
    if not isinstance(dicted, bool):
        raise ValueError("The 'dicted' parameter must be a boolean.")
    if not isinstance(weight_key, str):
        raise ValueError("The 'weight_key' parameter must be a string.")

    if weighted and dicted:
        raise ValueError("The 'weighted' and 'dicted' parameters cannot both be True.")

    adjacency = []
    for u in range(len(graph)):
        neighbors = []
        for v, attributes in graph[u].items():
            if weighted:
                neighbors.append((v, attributes.get(weight_key, 1.0)))
            elif dicted:
                neighbors.append((v, attributes))
            else:
                neighbors.append(v)
        adjacency.append(neighbors)

    return adjacency


def graph_to_edges_list(
    graph: GraphRepresentation,
    *,
    weighted: bool = False,
    weight_key: Optional[str] = "weight",
    dicted: bool = True,
    skip_validation=False
) -> Edges:
    r"""
    Convert a graph represented as a dictionary (``GraphRepresentation``) to a graph represented
    as an edge list (``Edges``).

    .. include:: /_static/rstdoc/edges_representation.rst

    .. include:: /_static/rstdoc/graph_representation.rst


    Parameters
    ----------
    graph : GraphRepresentation
        The graph represented as a dictionary.

    weighted : bool, optional (default: ``False``)
        Whether to represent the graph as ``List[Tuple[Integral, Integral, Real]]``.

    weight_key : Optional[str], optional (default: ``'weight'``)
        The key to use for accessing the weight of an edge in the graph representation.
        Ignored if ``weighted`` is False.

    dicted : bool, optional (default: ``False``)
        Whether to represent the graph as ``List[Tuple[Integral, Integral, Dict[str, Any]]]``.

    Returns
    -------
    edge_list : Edges
        The graph represented as an edge list.

    """
    if not skip_validation:
        assert_valid_graph(graph)
    if not isinstance(weighted, bool):
        raise ValueError("The 'weighted' parameter must be a boolean.")
    if not isinstance(dicted, bool):
        raise ValueError("The 'dicted' parameter must be a boolean.")
    if not isinstance(weight_key, str):
        raise ValueError("The 'weight_key' parameter must be a string.")

    if weighted and dicted:
        raise ValueError("The 'weighted' and 'dicted' parameters cannot both be True.")

    edges = []
    for u in range(len(graph)):
        for v, attributes in graph[u].items():
            if weighted:
                edges.append((u, v, attributes.get(weight_key, 1.0)))
            elif dicted:
                edges.append((u, v, attributes))
            else:
                edges.append((u, v))

    return edges


def adjacency_list_to_edges_list(
    adjacency: AdjacencyList, *, skip_validation=False
) -> Edges:
    r"""
    Convert a graph represented as an adjacency list (``AdjacencyList``) to a graph
    represented as an edge list (``Edges``).

    .. include:: /_static/rstdoc/adjacency_list_representation.rst

    .. include:: /_static/rstdoc/edges_representation.rst

    Parameters
    ----------
    adjacency : AdjacencyList
        The adjacency list to convert into an edge list.

    Returns
    -------
    edge_list : Edges
        The graph represented as an edge list.

    """
    if not skip_validation:
        assert_valid_adjacency_list(adjacency)

    return [
        (u, *v) if isinstance(v, tuple) else (u, v)
        for u, neighbors in enumerate(adjacency)
        for v in neighbors
    ]


def edges_list_to_adjacency_list(
    edges: Edges, n_vertices: Integral, *, skip_validation=False
) -> AdjacencyList:
    r"""
    Convert a graph represented as an edge list (``Edges``) to a graph represented
    as an adjacency list (``AdjacencyList``).

    .. include:: /_static/rstdoc/edges_representation.rst

    .. include:: /_static/rstdoc/adjacency_list_representation.rst


    Parameters
    ----------
    edges : Edges
        The edge list to convert into an adjacency list.

    n_vertices : Integral
        The number of vertices in the graph.


    Returns
    -------
    adjacency_list : AdjacencyList
        The graph represented as an adjacency list.

    """
    if not skip_validation:
        assert_valid_edges(edges, n_vertices)
    if not isinstance(n_vertices, Integral) or n_vertices < 0:
        raise ValueError("The 'n_vertices' parameter must be a non-negative integer.")

    adjacency = [[] for _ in range(n_vertices)]
    for edge in edges:
        if len(edge) == 2:
            u, v = edge
            adjacency[u].append(v)
        else:
            u, v, w = edge
            adjacency[u].append((v, w))
    return adjacency
