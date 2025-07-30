from __future__ import annotations
from typing import Any, Optional, Dict, List, Set, Tuple, Union
from collections import deque, defaultdict


class Graph:
    """A base graph class supporting both directed and undirected graphs."""

    def __init__(self, directed: bool = False) -> None:
        """Initialize the graph.

        Args:
            directed: Whether the graph is directed. Defaults to False.
        """
        self.directed = directed
        self.adjacency_list: Dict[Any, Dict[Any,
                                            Optional[float]]] = defaultdict(dict)
        self.vertices: Set[Any] = set()

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph.

        Args:
            vertex: The vertex to add.
        """
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency_list[vertex] = {}

    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its edges from the graph.

        Args:
            vertex: The vertex to remove.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")

        # Remove all edges to this vertex
        for neighbor in list(self.adjacency_list[vertex].keys()):
            self.remove_edge(vertex, neighbor)

        # Remove the vertex
        del self.adjacency_list[vertex]
        self.vertices.remove(vertex)

    def add_edge(self, v1: Any, v2: Any, weight: Optional[float] = None) -> None:
        """Add an edge between two vertices.

        Args:
            v1: The first vertex.
            v2: The second vertex.
            weight: Optional edge weight. Defaults to None.

        Raises:
            KeyError: If either vertex doesn't exist.
        """
        if v1 not in self.vertices or v2 not in self.vertices:
            raise KeyError("One or both vertices not found")

        self.adjacency_list[v1][v2] = weight
        if not self.directed:
            self.adjacency_list[v2][v1] = weight

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """Remove an edge between two vertices.

        Args:
            v1: The first vertex.
            v2: The second vertex.

        Raises:
            KeyError: If edge doesn't exist.
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list[v1]:
            raise KeyError(f"Edge {v1}-{v2} not found")

        del self.adjacency_list[v1][v2]
        if not self.directed:
            del self.adjacency_list[v2][v1]

    def has_vertex(self, vertex: Any) -> bool:
        """Check if a vertex exists in the graph.

        Args:
            vertex: The vertex to check.

        Returns:
            True if vertex exists, False otherwise.
        """
        return vertex in self.vertices

    def has_edge(self, v1: Any, v2: Any) -> bool:
        """Check if an edge exists between two vertices.

        Args:
            v1: The first vertex.
            v2: The second vertex.

        Returns:
            True if edge exists, False otherwise.
        """
        return v1 in self.adjacency_list and v2 in self.adjacency_list[v1]

    def get_vertices(self) -> List[Any]:
        """Get all vertices in the graph.

        Returns:
            A list of all vertices.
        """
        return list(self.vertices)

    def get_edges(self) -> List[Tuple[Any, Any, Optional[float]]]:
        """Get all edges in the graph.

        Returns:
            A list of tuples (v1, v2, weight) representing edges.
        """
        edges = []
        for v1 in self.adjacency_list:
            for v2, weight in self.adjacency_list[v1].items():
                if self.directed or (v2, v1, weight) not in edges:
                    edges.append((v1, v2, weight))
        return edges

    def degree(self, vertex: Any) -> int:
        """Get the degree of a vertex (number of edges).

        Args:
            vertex: The vertex to check.

        Returns:
            The degree of the vertex.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")
        return len(self.adjacency_list[vertex])

    def neighbors(self, vertex: Any) -> List[Any]:
        """Get all neighbors of a vertex.

        Args:
            vertex: The vertex to check.

        Returns:
            A list of neighboring vertices.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")
        return list(self.adjacency_list[vertex].keys())

    def dfs(self, start: Any) -> List[Any]:
        """Perform depth-first search starting from a vertex.

        Args:
            start: The starting vertex.

        Returns:
            A list of vertices in DFS order.

        Raises:
            KeyError: If start vertex doesn't exist.
        """
        if start not in self.vertices:
            raise KeyError(f"Vertex {start} not found")

        visited = []
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                # Push neighbors in reverse order to visit them in order
                stack.extend(reversed(self.neighbors(vertex)))
        return visited

    def bfs(self, start: Any) -> List[Any]:
        """Perform breadth-first search starting from a vertex.

        Args:
            start: The starting vertex.

        Returns:
            A list of vertices in BFS order.

        Raises:
            KeyError: If start vertex doesn't exist.
        """
        if start not in self.vertices:
            raise KeyError(f"Vertex {start} not found")

        visited = []
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.append(vertex)
                queue.extend(self.neighbors(vertex))
        return visited

    def is_connected(self) -> bool:
        """Check if the graph is connected (undirected graphs only).

        Returns:
            True if graph is connected, False otherwise.

        Raises:
            RuntimeError: If called on a directed graph.
        """
        if self.directed:
            raise RuntimeError(
                "Cannot check connectivity on directed graphs - use is_strongly_connected()")

        if not self.vertices:
            return True

        start = next(iter(self.vertices))
        visited = set(self.dfs(start))
        return len(visited) == len(self.vertices)

    def _has_cycle_util(self, vertex: Any, visited: Set[Any], parent: Optional[Any]) -> bool:
        """Utility function for cycle detection (undirected graphs)."""
        visited.add(vertex)
        for neighbor in self.neighbors(vertex):
            if neighbor not in visited:
                if self._has_cycle_util(neighbor, visited, vertex):
                    return True
            elif parent != neighbor:
                return True
        return False

    def _has_cycle_directed_util(self, vertex: Any, visited: Set[Any], rec_stack: Set[Any]) -> bool:
        """Utility function for cycle detection (directed graphs)."""
        visited.add(vertex)
        rec_stack.add(vertex)

        for neighbor in self.neighbors(vertex):
            if neighbor not in visited:
                if self._has_cycle_directed_util(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(vertex)
        return False

    def is_cyclic(self) -> bool:
        """Check if the graph contains any cycles.

        Returns:
            True if graph contains cycles, False otherwise.
        """
        if not self.directed:
            visited = set()
            for vertex in self.vertices:
                if vertex not in visited:
                    if self._has_cycle_util(vertex, visited, None):
                        return True
            return False
        else:
            visited = set()
            rec_stack = set()
            for vertex in self.vertices:
                if vertex not in visited:
                    if self._has_cycle_directed_util(vertex, visited, rec_stack):
                        return True
            return False

    def topological_sort(self) -> List[Any]:
        """Perform topological sort (for DAGs only).

        Returns:
            A list of vertices in topological order.

        Raises:
            RuntimeError: If graph is not a DAG (contains cycles).
        """
        if not self.directed:
            raise RuntimeError(
                "Topological sort only applies to directed graphs")
        if self.is_cyclic():
            raise RuntimeError(
                "Graph contains cycles - cannot perform topological sort")

        in_degree = {v: 0 for v in self.vertices}
        for v in self.vertices:
            for neighbor in self.neighbors(v):
                in_degree[neighbor] += 1

        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        top_order = []

        while queue:
            vertex = queue.popleft()
            top_order.append(vertex)
            for neighbor in self.neighbors(vertex):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(top_order) != len(self.vertices):
            raise RuntimeError(
                "Graph contains cycles - topological sort not possible")

        return top_order

    @property
    def vertex_count(self) -> int:
        """Get the number of vertices in the graph.

        Returns:
            The vertex count.
        """
        return len(self.vertices)

    @property
    def edge_count(self) -> int:
        """Get the number of edges in the graph.

        Returns:
            The edge count.
        """
        return len(self.get_edges())

    def __str__(self) -> str:
        """Return string representation of the graph.

        Returns:
            A string representation of the graph.
        """
        directed_str = "Directed" if self.directed else "Undirected"
        return f"{directed_str} Graph with {self.vertex_count} vertices and {self.edge_count} edges"
