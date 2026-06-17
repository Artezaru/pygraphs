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
from .__version__ import __version__
from typing import Union, Sequence, Dict, Optional, Any, Tuple
from numbers import Integral, Real
from .types import (
    Edges,
    AdjacencyList,
    GraphRepresentation,
)
from .conversion import (
    adjacency_list_to_graph,
    edges_list_to_graph,
    graph_to_adjacency_list,
    graph_to_edges_list,
)
import copy
from .exeptions import (
    assert_valid_graph,
    assert_valid_vertex,
    assert_valid_weight,
    assert_valid_edges,
)


class Graph:
    r"""
    Graph class representing a generic **directed** graph with edge attributes.

    The graph is stored internally as a ``Dict[int, Dict[int, Dict[str, Any]]]``
    (GraphRepresentation) where
    the keys of the outer dictionary are the vertex indices, the keys of the inner dictionary
    are the neighboring vertex indices,
    and the values of the inner dictionary are dictionaries containing edge attributes
    such as weight.

    The Graph class provides methods to convert between adjacency list and edge list representations,
    as well as methods to check add edges and vertices. Consider
    using ``from_adjacency`` and ``from_edges`` class methods to create a
    Graph object from an adjacency list or edge list representation, respectively.


    Parameters
    ----------
    graph : GraphRepresentation
        The graph represented as a dictionary where the keys are vertex indices
        and the values are dictionaries mapping neighboring vertex indices to edge attributes.

    Examples
    --------
    Example of initializing a Graph object with an adjacency list representation:

    .. code-block:: python
       :linenos:

       from pygraphs import Graph

       adjacency_list = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], []]
       graph = Graph.from_adjacency(adjacency_list)


    """

    def __init__(self, graph: GraphRepresentation, skip_validation: bool = False):
        if not skip_validation:
            assert_valid_graph(Graph)
        self._graph = graph

    @classmethod
    def from_adjacency(cls, adjacency: AdjacencyList, **kwargs) -> Graph:
        r"""
        Create a Graph object from an adjacency list representation.

        .. include:: /_static/rstdoc/adjacency_list_representation.rst

        .. seealso::

            - :func:`pygraphs.adjacency_list_to_graph` to assemble the graph from an adjacency list.

        Parameters
        ----------
        adjacency : AdjacencyList
            The graph represented as an adjacency list.

        **kwargs
            Additionals arguments to pass to the conversion function.

        Returns
        -------
        Graph
            A Graph object representing the given adjacency list.

        """
        return cls(
            graph=adjacency_list_to_graph(adjacency, **kwargs), skip_validation=True
        )

    @classmethod
    def from_edges(cls, edges: Edges, n_vertices: Integral, **kwargs) -> Graph:
        r"""
        Create a Graph object from an edge list representation.

        .. include:: /_static/rstdoc/edges_representation.rst

        .. seealso::

            - :func:`pygraphs.edges_list_to_graph` to assemble the graph from an edges list.

        Parameters
        ----------
        edges : Union[Edges, WeightedEdges]
            The graph represented as an edge list.

        n_vertices : Integral
            The number of vertices in the graph. This is needed to determine the size of the adjacency list.

        **kwargs
            Additionals arguments to pass to the conversion function.

        Returns
        -------
        Graph
            A Graph object representing the given edge list.

        """
        return cls(
            graph=edges_list_to_graph(edges, n_vertices, **kwargs), skip_validation=True
        )

    def to_adjacency(self, **kwargs) -> AdjacencyList:
        r"""
        Get the adjacency list representation of the graph.

        .. include:: /_static/rstdoc/adjacency_list_representation.rst

        .. seealso::

            - :func:`pygraphs.graph_to_adjacency_list` to assemble the graph into an adjacency list.

        Parameters
        ----------
        **kwargs
            Additionals arguments to pass to the conversion function.

        Returns
        -------
        Union[AdjacencyList, WeightedAdjacencyList]
            The adjacency list representation of the graph.

        """
        return graph_to_adjacency_list(self._graph, **kwargs)

    def to_edges(self, **kwargs) -> Edges:
        r"""
        Get the edge list representation of the graph.

        .. include:: /_static/rstdoc/edges_representation.rst

        .. seealso::

            - :func:`pygraphs.graph_to_edges_list` to assemble the graph into an edges list.

        Parameters
        ----------
        **kwargs
            Additionals arguments to pass to the conversion function.

        Returns
        -------
        Union[Edges, WeightedEdges]
            The edge list representation of the graph.

        """
        return graph_to_edges_list(self._graph, **kwargs)

    @property
    def n_vertices(self) -> int:
        r"""
        Get the number of vertices in the graph.

        Returns
        -------
        int
            The number of vertices in the graph.
        """
        return len(self._graph)

    def __len__(self) -> int:
        r"""
        Get the number of vertices in the graph using the built-in len() function.

        Returns
        -------
        int
            The number of vertices in the graph.
        """
        return self.n_vertices

    @property
    def n_edges(self) -> int:
        r"""
        Get the number of edges in the graph for the **directed** graph.

        For an undirected graph, the number of edges is half the number of
        edges in the directed version of the graph.

        .. code-block:: python
            :linenos:

            if graph.is_directed():
                n_edges = graph.n_edges

            else:
                n_edges = graph.n_edges // 2


        Returns
        -------
        int
            The number of edges in the graph.
        """
        return sum(len(nbr) for nbr in self._graph.values())

    def add_vertex(self) -> None:
        r"""
        Add a vertex to the graph. The new vertex will have an index equal
        to the current number of vertices in the graph.

        Returns
        -------
        None
            This method does not return anything.
        """
        new_vertex_index = self.n_vertices
        self._graph[new_vertex_index] = {}

    def add_n_vertices(self, n: Integral) -> None:
        r"""
        Add multiple vertices to the graph. The new vertices will have indices
        starting from the current number of vertices in the graph.

        Parameters
        ----------
        n : Integral
            The number of vertices to add.

        Returns
        -------
        None
            This method does not return anything.
        """
        for _ in range(n):
            self.add_vertex()

    def remove_vertex(self, vertex: Integral) -> None:
        r"""
        Remove a vertex from the graph. This will also remove all
        edges incident to the vertex.

        .. important::

            Removing a vertex will shift the indices of all vertices with
            indices greater than the removed vertex down by 1.

        Parameters
        ----------
        vertex : Integral
            The index of the vertex to remove.

        Returns
        -------
        None
            This method does not return anything.
        """
        assert_valid_vertex(vertex, self.n_vertices, integer=True)

        new_graph = {}
        for u, nbr in self._graph.items():
            if u == vertex:
                continue  # skip the removed vertex

            new_u = u - 1 if u > vertex else u
            new_graph[new_u] = {}

            for v, edge_data in nbr.items():
                if v == vertex:
                    continue  # skip edges incident to the removed vertex

                new_v = v - 1 if v > vertex else v
                new_graph[new_u][new_v] = copy.deepcopy(edge_data)

        self._graph = new_graph

    def remove_n_vertices(self, vertices: Sequence[Integral]) -> None:
        r"""
        Remove multiple vertices from the graph. This will also remove all
        edges incident to the removed vertices.

        .. important::

            Removing vertices will shift the indices of all vertices with
            indices greater than the removed vertices down by the number of removed vertices.

        Parameters
        ----------
        vertices : Sequence[Integral]
            A sequence of vertex indices to remove.


        Returns
        -------
        None
            This method does not return anything.
        """
        if not isinstance(vertices, Sequence):
            raise ValueError("vertices must be a sequence of vertex indices.")
        for vertex in vertices:
            assert_valid_vertex(vertex, self.n_vertices, integer=True)

        vertices_to_remove = set(vertices)
        cumsum = [0] * (self.n_vertices + 1)
        for vertex in vertices_to_remove:
            cumsum[vertex + 1] = 1
        for i in range(1, len(cumsum)):
            cumsum[i] += cumsum[i - 1]

        new_graph = {}
        for u, nbr in self._graph.items():
            if u in vertices_to_remove:
                continue  # skip the removed vertex

            new_u = (
                u - cumsum[u]
            )  # shift down by the number of removed vertices before u
            new_graph[new_u] = {}

            for v, edge_data in nbr.items():
                if v in vertices_to_remove:
                    continue  # skip edges incident to the removed vertex

                new_v = (
                    v - cumsum[v]
                )  # shift down by the number of removed vertices before v
                new_graph[new_u][new_v] = copy.deepcopy(edge_data)

        self._graph = new_graph

    def add_edge(
        self,
        u: Integral,
        v: Integral,
        data: Optional[Union[Real, Dict[str, Any]]] = None,
        *,
        weight_key: str = "weight",
    ) -> None:
        r"""
        Add an edge to the graph. If the graph is weighted, a weight must be provided.

        Parameters
        ----------
        u : Integral
            The index of the source vertex.

        v : Integral
            The index of the target vertex.

        data : Union[Real, Dict[str, Any]], (default: ``None``)
            The edge attributes. If a real value is given, it will be treated as a weight.

        weight_key : str, optional (default: ``'weight'``)
            The key to use for storing edge weights in the graph
            representation.

        Returns
        -------
        None
            This method does not return anything.
        """
        assert_valid_vertex(u, self.n_vertices, integer=True)
        assert_valid_vertex(v, self.n_vertices, integer=True)

        if not isinstance(weight_key, str):
            raise ValueError("weight_key must be a string")

        if v in self._graph[u]:
            raise ValueError(f"Edge ({u}, {v}) already exists.")

        if data is None:
            data = {}
        if not isinstance(data, dict):
            assert_valid_weight(data, floating=True)
            data = {weight_key: data}
        if not all(isinstance(w, str) for w in data.keys()):
            raise ValueError("Attributes dict keys must be strings")

        self._graph[u][v] = data

    def add_edges(
        self,
        edges: Edges,
        *,
        weight_key: str = "weight",
    ) -> None:
        r"""
        Add multiple edges to the graph.

        Parameters
        ----------
        edges : Edges
            The edges to add to the graph.

        weight_key : str, optional (default: ``'weight'``)
            The key to use for storing edge weights in the graph
            representation.

        Returns
        -------
        None
            This method does not return anything.
        """
        assert_valid_edges(edges, n_vertices=self.n_vertices)

        for edge in edges:
            self.add_edge(*edge, weight_key=weight_key)

    def remove_edge(self, u: Integral, v: Integral) -> None:
        r"""
        Remove an edge from the graph.

        Parameters
        ----------
        u : Integral
            The index of the source vertex.

        v : Integral
            The index of the target vertex.

        Returns
        -------
        None
            This method does not return anything.
        """
        assert_valid_vertex(u, self.n_vertices, integer=True)
        assert_valid_vertex(v, self.n_vertices, integer=True)

        if v not in self._graph[u]:
            raise ValueError(f"Edge ({u}, {v}) does not exist.")
        del self._graph[u][v]

    def remove_edges(self, edges: Sequence[Tuple[Integral, Integral]]) -> None:
        r"""
        Remove multiple edges from the graph.

        Parameters
        ----------
        edges : Sequence[Tuple[Integral, Integral]]
            A sequence of edges to remove. Each edge should be represented as a tuple of the form :math:`(u, v)`,
            where :math:`u` and :math:`v` are vertex indices.

        Returns
        -------
        None
            This method does not return anything.
        """
        if not isinstance(edges, Sequence):
            raise ValueError("edges must be a sequence of edges.")
        for edge in edges:
            self.remove_edge(*edge)

    def __str__(self) -> str:
        r"""
        Get a string representation of the graph.

        Returns
        -------
        str
            A string representation of the graph.
        """
        return f"Graph(n_vertices={self.n_vertices}, n_edges={self.n_edges}"

    def is_directed(
        self, weight_match: bool = True, weight_key: str = "weight"
    ) -> bool:
        r"""
        Check if the graph is directed.

        A graph is considered undirected if every edge (u, v)
        has a corresponding edge (v, u). Otherwise it is directed.

        If ``weight_match`` is True, then the graph is considered undirected
        only if every edge (u, v) has a corresponding edge (v, u) with the same weight.
        Otherwise, the weights of the edges are ignored when checking if the graph is directed.

        By convention, an empty graph is considered undirected.

        Parameters
        ----------
        weight_match : bool, optional (default: ``True``)
            Whether to consider the weights of the edges when checking if the graph is directed.

        weight_key : str, optional (default: ``'weight'``)
            The key to use for storing edge weights in the graph
            representation.

        Returns
        -------
        bool
            True if the graph is directed, False otherwise.
        """
        if not isinstance(weight_key, str):
            raise ValueError("weight_key must be a string")

        if self.n_edges == 0:
            return False

        for u, nbr in self._graph.items():
            for v, edge_data in nbr.items():
                if u not in self._graph[v]:
                    return True
                if weight_match:
                    if self._graph[v][u].get(weight_key, 1.0) != edge_data.get(
                        weight_key, 1.0
                    ):
                        return True

        return False

    def is_weight_symmetric(
        self, weight_key: str = "weight", *, atol: float = 1e-6
    ) -> bool:
        r"""
        Check if the graph has symmetric weights, meaning that for every edge (u, v) with weight w,
        if there is a corresponding edge (v, u), it must also have weight w.

        By convention, an empty graph is considered to have symmetric weights.

        Parameters
        ----------
        weight_key : str, optional (default: ``'weight'``)
            The key to use for storing edge weights in the graph
            representation.

        atol: float (default: ``1e-6``)
            Absolute tolerance.

        Returns
        -------
        bool
            True if the graph has symmetric weights, False otherwise.
        """
        if not isinstance(weight_key, str):
            raise ValueError("weight_key must be a string")

        if self.n_edges == 0:
            return True

        for u, nbr in self._graph.items():
            for v, edge_data in nbr.items():
                if u in self._graph[v]:
                    if (
                        abs(
                            self._graph[v][u].get(weight_key, 1.0)
                            - edge_data.get(weight_key, 1.0)
                        )
                        > atol
                    ):
                        return False

        return True

    def to_undirected(self) -> Graph:
        """
        Return a new graph that is the undirected version of the current graph by adding
        a reverse edge for each edge in the original graph.

        If the graph is already undirected, a copy of the graph is returned.

        .. warning::

            If two edges wexist between the same pair of vertices and differents attributes
            in the original graph, an error will be raised since it is not possible
            to create an undirected graph with symmetric data in this case.

        Returns
        -------
        Graph
            A new Graph object representing the undirected version of the original graph.
        """
        new_graph = {i: {} for i in range(self.n_vertices)}
        for u, nbr in self._graph.items():
            for v, edge_data in nbr.items():
                if u in new_graph[v]:
                    if new_graph[v][u] != edge_data:
                        raise ValueError(
                            f"Cannot create undirected graph without symmetric attributes because of edges ({u}, {v}) and ({v}, {u}) having different attributes."
                        )
                new_graph[u][v] = copy.deepcopy(edge_data)
                new_graph[v][u] = copy.deepcopy(edge_data)  # add reverse edge

        return Graph(new_graph, skip_validation=True)

    def to_clean(self) -> Graph:
        """
        Return the same graph without edge attributes.

        Returns
        -------
        Graph
            A new Graph object representing the clean version of the original graph.
        """
        new_graph = {i: {} for i in range(self.n_vertices)}
        for u, nbr in self._graph.items():
            for v, edge_data in nbr.items():
                new_graph[u][v] = {}

        return Graph(new_graph, skip_validation=True)

    def to_reversed(self) -> Graph:
        """
        Return the same graph with all edge reversed.
        Returns
        -------
        Graph
            A new Graph object representing the reserved version of the original graph.
        """
        new_graph = {i: {} for i in range(self.n_vertices)}
        for u, nbr in self._graph.items():
            for v, edge_data in nbr.items():
                new_graph[v][u] = edge_data

        return Graph(new_graph, skip_validation=True)
