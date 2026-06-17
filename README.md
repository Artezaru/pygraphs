# pygraphs

## Description

`pygraphs` provides tools to perform BFS, DFS, Dijkstra, and more on
graphs. The package support weighted graphs, directed graphs but not multigraphs.

## Authors

- Artezaru <artezaru.github@proton.me>

- **Git Plateform**: https://github.com/Artezaru/pygraphs.git
- **Online Documentation**: https://Artezaru.github.io/pygraphs

## Installation

Install with pip

```
pip install pygraphs
```

```
pip install git+https://github.com/Artezaru/pygraphs.git
```

Clone with git

```
git clone https://github.com/Artezaru/pygraphs.git
```

## Usage

This section will guide you through the basic usage of the `pygraphs` package.
Several examples are available on the online documentation.

### Construct a graph

To create a graph, you can provide the edges or the adjacency : 

```python
from pygraphs import Graph

graph = [[1, 2], [0, 2], [0, 1, 3], [2, 4], [3], [6], [5]]
undirected_graph = Graph.from_adjacency(graph)
```

### Perform operations on graphs

Several algorithms are availables to perform basic operations on graphs. 
For example, the following compute the adjacency matrix by BFS:

```python
from pygraphs import bfs_matrix

adjacency_matrix = bfs_matrix(undirected_graph)
print(f"adjacency_matrix (shape={len(adjacency_matrix)}x{len(adjacency_matrix[0])}):")
print(adjacency_matrix)

# Expected output:
# adjacency_matrix (shape=(7x7)):
# [[ 0  1  1  2  3 -1 -1]
#  [ 1  0  1  2  3 -1 -1]
#  [ 1  1  0  1  2 -1 -1]
#  [ 2  2  1  0  1 -1 -1]
#  [ 3  3  2  1  0 -1 -1]
#  [-1 -1 -1 -1 -1  0  1]
#  [-1 -1 -1 -1 -1  1  0]]
```

## License

Copyright 2026 Artezaru

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
