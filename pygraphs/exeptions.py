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

from typing import Any, Sequence
from numbers import Integral, Real


class InvalidGraphError(Exception):
    """
    Exception raised when an invalid graph is provided to a function.
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidGraphRepresentationError(InvalidGraphError):
    """
    Raised when a graph representation is invalid.
    """

    def __init__(self):
        message = f"Invalid graph representation. Expected a Dict[int -> Dict[int -> Dict[str -> Any]]]."
        super().__init__(message)


class InvalidVertexError(InvalidGraphError):
    """
    Exception raised when a graph contains an invalid vertex
    (e.g., a vertex index that is out of bounds).
    """

    def __init__(self, vertex, n_vertices=None):
        if n_vertices is not None:
            message = f"Invalid vertex. Expected a non-negative integer vertex index that is within the bounds of the graph (0 to {n_vertices - 1}). Got: {vertex}"
        else:
            message = f"Invalid vertex. Expected a non-negative integer vertex index. Got: {vertex}"
        super().__init__(message)


class InvalidWeightError(InvalidGraphError):
    """
    Raised when an edge has an invalid weight.
    """

    def __init__(self, weight):
        message = f"Invalid weight. Expected a non-negative number. Got: {weight}"
        super().__init__(message)


class DuplicateEdgeError(InvalidGraphError):
    """
    Raised when a graph contains duplicate edges.
    """

    def __init__(self, edge):
        message = f"Duplicate edge found: {edge}"
        super().__init__(message)


class InvalidEdgesError(InvalidGraphError):
    """
    Raised when an edge list is invalid.
    """

    def __init__(self):
        message = f"Invalid edge list graph representation. Expected a List[Tuple[int, int]] for unweighted graph, List[Tuple[int, int, float]] for weighted graph or List[Tuple[int, int, Dict[str -> Any]]] for graphs with custom attributes."
        super().__init__(message)


class InvalidAdjacencyListError(InvalidGraphError):
    """
    Raised when an adjacency list is invalid.
    """

    def __init__(self):
        message = f"Invalid adjacency list graph representation. Expected a List[List[int]] for unweighted graph, List[List[Tuple[int, float]]] for weighted graph or List[List[Tuple[int, Dict[str, Any]]]] for graphs with custom attributes."
        super().__init__(message)


def assert_valid_vertex(vertex: Any, n_vertices: Integral, integer=False):
    """
    Assert that the given vertex is valid. If the vertex is invalid, raise an appropriate exception.

    Parameters
    ----------
    vertex : Any
        The vertex to check.

    n_vertices : Integral
        The number of vertices in the graph. This is needed to check if the vertex index is valid.

    Raises
    ------
    InvalidVertexError
        If the vertex is invalid.
    """
    if not isinstance(vertex, Integral):
        raise InvalidVertexError(vertex, n_vertices)
    if integer and not isinstance(vertex, int):
        raise InvalidVertexError(vertex, n_vertices)
    if vertex < 0 or vertex >= n_vertices:
        raise InvalidVertexError(vertex, n_vertices)


def assert_valid_weight(weight: Any, floating=False):
    """
    Assert that the given weight is valid. If the weight is invalid, raise an appropriate exception.

    Parameters
    ----------
    weight : Any
        The weight to check.

    Raises
    ------
    InvalidWeightError
        If the weight is invalid.
    """
    if not (isinstance(weight, Real) and weight >= 0):
        raise InvalidWeightError(weight)
    if floating and not isinstance(weight, float):
        raise InvalidWeightError(weight)


def assert_valid_graph(graph: Any) -> None:
    """
    Assert that the given graph is valid. If the graph is invalid, raise an appropriate exception.

    Parameters
    ----------
    graph : Any
        The graph to check.

    Raises
    ------
    InvalidGraphError
        If the graph is invalid.
    """
    if not isinstance(graph, dict):
        raise InvalidGraphRepresentationError()
    n_vertices = len(graph)
    for u, neighbors in graph.items():
        assert_valid_vertex(u, n_vertices, integer=True)
        if not isinstance(neighbors, dict):
            raise InvalidGraphRepresentationError()
        for v, edge_data in neighbors.items():
            assert_valid_vertex(v, n_vertices, integer=True)
            if not isinstance(edge_data, dict):
                raise InvalidGraphRepresentationError()
            if not all(isinstance(key, str) for key in edge_data.keys()):
                raise InvalidGraphRepresentationError()


def assert_valid_graph_weights(graph: Any, weight_key: str) -> None:
    """Assert the weights of a graĥ are correct !"""
    n_vertices = len(graph)
    for u, neighbors in graph.items():
        for v, edge_data in neighbors.items():
            if weight_key in edge_data:
                assert_valid_weight(edge_data[weight_key], floating=True)


def assert_valid_edges(edges: Any, n_vertices: Integral) -> None:
    """
    Assert that the given edge list is valid.
    If the edge list is invalid, raise an appropriate exception.

    Parameters
    ----------
    edges : Any
        The edge list to check.

    n_vertices : Integral
        The number of vertices in the graph. This is needed to check if vertex indices are valid.

    Raises
    ------
    InvalidEdgesListError
        If the edge list is invalid.
    """
    if not isinstance(edges, Sequence):
        raise InvalidEdgesError()
    if not isinstance(n_vertices, Integral) or n_vertices < 0:
        raise InvalidGraphError(
            f"Invalid number of vertices: {n_vertices}. Expected a non-negative integer."
        )

    any_weighted = False
    any_unweighted = False
    any_dict = False
    seen_edges = set()

    for edge in edges:
        if not isinstance(edge, tuple):
            raise InvalidEdgesError()
        if len(edge) == 2:
            any_unweighted = True
            u, v = edge
            assert_valid_vertex(u, n_vertices)
            assert_valid_vertex(v, n_vertices)
        elif len(edge) == 3:
            u, v, w = edge
            assert_valid_vertex(u, n_vertices)
            assert_valid_vertex(v, n_vertices)
            if isinstance(w, dict):
                any_dict = True
                if not all(isinstance(key, str) for key in w.keys()):
                    raise InvalidEdgesError()
            else:
                any_weighted = True
                assert_valid_weight(w, floating=True)
        else:
            raise InvalidEdgesError()

        edge_key = (u, v)
        if edge_key in seen_edges:
            raise DuplicateEdgeError(edge_key)
        seen_edges.add(edge_key)

    if sum([any_weighted, any_unweighted, any_dict]) > 1:
        raise InvalidEdgesError()


def assert_valid_adjacency_list(adjacency: Any) -> None:
    """
    Assert that the given adjacency list is valid. If the adjacency list is invalid, raise an appropriate exception.

    Parameters
    ----------
    adjacency : Any
        The adjacency list to check.

    Raises
    ------
    InvalidAdjacencyListError
        If the adjacency list is invalid.
    """
    if not isinstance(adjacency, Sequence):
        raise InvalidAdjacencyListError()
    n_vertices = len(adjacency)

    any_dict = False
    any_weighted = False
    any_unweighted = False
    seen_edges = set()

    for u, neighbors in enumerate(adjacency):
        if not isinstance(neighbors, Sequence):
            raise InvalidAdjacencyListError()
        for neighbor in neighbors:
            if isinstance(neighbor, Integral):
                any_unweighted = True
                v = neighbor
                assert_valid_vertex(v, n_vertices)
            elif isinstance(neighbor, tuple) and len(neighbor) == 2:
                v, w = neighbor
                assert_valid_vertex(v, n_vertices)
                if isinstance(w, dict):
                    any_dict = True
                    if not all(isinstance(key, str) for key in w.keys()):
                        raise InvalidAdjacencyListError()
                else:
                    any_weighted = True
                    assert_valid_weight(w, floating=True)
            else:
                raise InvalidAdjacencyListError()

            edge_key = (u, v)
            if edge_key in seen_edges:
                raise DuplicateEdgeError(edge_key)
            seen_edges.add(edge_key)

    if sum([any_weighted, any_unweighted, any_dict]) > 1:
        raise InvalidAdjacencyListError()
