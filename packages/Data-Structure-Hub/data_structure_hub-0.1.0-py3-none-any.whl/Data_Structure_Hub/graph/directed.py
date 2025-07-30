from __future__ import annotations
from typing import Any, Dict, List, Set, Tuple, Optional
from collections import deque, defaultdict
from graph import Graph


class DirectedGraph(Graph):
    """A directed graph implementation with additional directed graph algorithms."""

    def __init__(self) -> None:
        """Initialize a directed graph."""
        super().__init__(directed=True)
        self.in_edges: Dict[Any, Dict[Any, Optional[float]]
                            ] = defaultdict(dict)

    def add_edge(self, v1: Any, v2: Any, weight: Optional[float] = None) -> None:
        """Add a directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The target vertex.
            weight: Optional edge weight. Defaults to None.

        Raises:
            KeyError: If either vertex doesn't exist.
        """
        super().add_edge(v1, v2, weight)
        self.in_edges[v2][v1] = weight

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """Remove the directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The target vertex.

        Raises:
            KeyError: If edge doesn't exist.
        """
        super().remove_edge(v1, v2)
        del self.in_edges[v2][v1]

    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its incoming/outgoing edges.

        Args:
            vertex: The vertex to remove.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")

        # Remove all outgoing edges
        for neighbor in list(self.adjacency_list[vertex].keys()):
            self.remove_edge(vertex, neighbor)

        # Remove all incoming edges
        for source in list(self.in_edges[vertex].keys()):
            self.remove_edge(source, vertex)

        # Remove the vertex
        del self.adjacency_list[vertex]
        del self.in_edges[vertex]
        self.vertices.remove(vertex)

    def in_degree(self, vertex: Any) -> int:
        """Get the in-degree of a vertex (number of incoming edges).

        Args:
            vertex: The vertex to check.

        Returns:
            The in-degree of the vertex.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")
        return len(self.in_edges[vertex])

    def out_degree(self, vertex: Any) -> int:
        """Get the out-degree of a vertex (number of outgoing edges).

        Args:
            vertex: The vertex to check.

        Returns:
            The out-degree of the vertex.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        return super().degree(vertex)

    def transpose(self) -> DirectedGraph:
        """Return the transpose of the graph (all edges reversed).

        Returns:
            A new DirectedGraph instance representing the transpose.
        """
        transposed = DirectedGraph()
        for vertex in self.vertices:
            transposed.add_vertex(vertex)

        for v1 in self.adjacency_list:
            for v2, weight in self.adjacency_list[v1].items():
                transposed.add_edge(v2, v1, weight)

        return transposed

    def _dfs_finish_times(self, vertex: Any, visited: Set[Any], stack: List[Any]) -> None:
        """Helper DFS for Kosaraju's algorithm to record finish times."""
        visited.add(vertex)
        for neighbor in self.neighbors(vertex):
            if neighbor not in visited:
                self._dfs_finish_times(neighbor, visited, stack)
        stack.append(vertex)

    def _dfs_scc(self, vertex: Any, visited: Set[Any], component: List[Any]) -> None:
        """Helper DFS for Kosaraju's algorithm to find SCCs."""
        visited.add(vertex)
        component.append(vertex)
        for neighbor in self.in_edges[vertex]:
            if neighbor not in visited:
                self._dfs_scc(neighbor, visited, component)

    def strongly_connected_components(self) -> List[List[Any]]:
        """Find all strongly connected components using Kosaraju's algorithm.

        Returns:
            A list of lists, where each inner list represents an SCC.
        """
        # First pass to record finish times
        visited = set()
        stack = []
        for vertex in self.vertices:
            if vertex not in visited:
                self._dfs_finish_times(vertex, visited, stack)

        # Second pass on transposed graph in reverse finish order
        transposed = self.transpose()
        visited = set()
        sccs = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                component = []
                transposed._dfs_scc(vertex, visited, component)
                sccs.append(component)
        return sccs

    def is_strongly_connected(self) -> bool:
        """Check if the graph is strongly connected.

        Returns:
            True if the graph is strongly connected, False otherwise.
        """
        if not self.vertices:
            return True

        sccs = self.strongly_connected_components()
        return len(sccs) == 1

    def topological_sort_kahn(self) -> List[Any]:
        """Perform topological sort using Kahn's algorithm.

        Returns:
            A list of vertices in topological order.

        Raises:
            RuntimeError: If graph contains cycles.
        """
        in_degree = {v: self.in_degree(v) for v in self.vertices}
        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        top_order = []
        count = 0

        while queue:
            vertex = queue.popleft()
            top_order.append(vertex)
            count += 1

            for neighbor in self.neighbors(vertex):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if count != len(self.vertices):
            raise RuntimeError("Graph contains at least one cycle")
        return top_order

    def get_incoming_edges(self, vertex: Any) -> List[Tuple[Any, Optional[float]]]:
        """Get all incoming edges to a vertex.

        Args:
            vertex: The target vertex.

        Returns:
            A list of tuples (source_vertex, weight) representing incoming edges.

        Raises:
            KeyError: If vertex doesn't exist.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Vertex {vertex} not found")
        return [(v, weight) for v, weight in self.in_edges[vertex].items()]
