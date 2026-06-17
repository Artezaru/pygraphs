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

from .__version__ import __version__

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
    adjacency_list_to_edges_list,
    edges_list_to_adjacency_list,
)

from .graph import Graph

from .bfs import (
    bfs,
    bfs_k_disk,
    bfs_k_annulus,
    bfs_k_ring,
    bfs_distances,
    bfs_shortest_path,
    bfs_shortest_distance,
    bfs_reachable,
    bfs_is_reachable,
    bfs_components,
    bfs_matrix,
)


from .dfs import dfs, dfs_is_reachable, dfs_reachable, dfs_components

from .scc import kosaraju_components, tarjan_components

from .dijkstra import (
    dijkstra,
    dijkstra_distances,
    dijkstra_k_annulus,
    dijkstra_k_disk,
    dijkstra_shortest_path,
    dijkstra_shortest_distance,
    dijkstra_matrix,
)
