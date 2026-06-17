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

from numbers import Integral, Real
from typing import Tuple, TypeAlias, Sequence, Dict, Any, Union

GraphRepresentation: TypeAlias = Dict[Integral, Dict[Integral, Dict[str, Any]]]

Edges: TypeAlias = Union[
    Sequence[Tuple[Integral, Integral]],  # Unweighted
    Sequence[Tuple[Integral, Integral, Real]],  # Weighted
    Sequence[Tuple[Integral, Integral, Dict[str, Any]]],  # Custom attributes
]

AdjacencyList: TypeAlias = Union[
    Sequence[Sequence[Integral]],  # Unweighted
    Sequence[Sequence[Tuple[Integral, Real]]],  # Weighted
    Sequence[Sequence[Tuple[Integral, Dict[str, Any]]]],  # Custom attributes
]
