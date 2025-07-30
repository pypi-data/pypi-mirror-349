from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional, Union
from collections import defaultdict, deque
import heapq
import math
from graph import Graph


class WeightedGraph(Graph):
    """A weighted graph implementation extending the base Graph class."""

    def __init__(self, directed: bool = False) -> None:
        """Initialize a weighted graph.

        Args:
            directed: Whether the graph is directed. Defaults to False.
        """
        super().__init__(directed)
        self.weights: Dict[Tuple[Any, Any], float] = {}

    def add_edge(self, v1: Any, v2: Any, weight: float = 1.0) -> None:
        """Add a weighted edge between two vertices.

        Args:
            v1: The first vertex.
            v2: The second vertex.
            weight: The edge weight. Defaults to 1.0.

        Raises:
            KeyError: If either vertex doesn't exist.
            ValueError: If weight is not numeric.
        """
        if not isinstance(weight, (int, float)):
            raise ValueError("Edge weight must be numeric")

        super().add_edge(v1, v2, weight)
        self.weights[(v1, v2)] = weight
        if not self.directed:
            self.weights[(v2, v1)] = weight

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """Remove an edge between two vertices.

        Args:
            v1: The first vertex.
            v2: The second vertex.

        Raises:
            KeyError: If edge doesn't exist.
        """
        super().remove_edge(v1, v2)
        del self.weights[(v1, v2)]
        if not self.directed:
            del self.weights[(v2, v1)]

    def get_edge_weight(self, v1: Any, v2: Any) -> float:
        """Get the weight of an edge.

        Args:
            v1: The first vertex.
            v2: The second vertex.

        Returns:
            The edge weight.

        Raises:
            KeyError: If edge doesn't exist.
        """
        if (v1, v2) not in self.weights:
            raise KeyError(f"Edge {v1}-{v2} not found")
        return self.weights[(v1, v2)]

    def dijkstra(self, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
        """Compute shortest paths using Dijkstra's algorithm.

        Args:
            start: The starting vertex.

        Returns:
            A tuple of (distance, predecessor) dictionaries.

        Raises:
            KeyError: If start vertex doesn't exist.
            ValueError: If negative weights are detected.
        """
        if start not in self.vertices:
            raise KeyError(f"Vertex {start} not found")

        # Check for negative weights
        if any(w < 0 for w in self.weights.values()):
            raise ValueError(
                "Dijkstra cannot handle negative weights - use Bellman-Ford")

        distances = {v: math.inf for v in self.vertices}
        predecessors = {v: None for v in self.vertices}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            current_dist, current_vertex = heapq.heappop(heap)
            if current_dist > distances[current_vertex]:
                continue

            for neighbor in self.neighbors(current_vertex):
                weight = self.get_edge_weight(current_vertex, neighbor)
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(heap, (distance, neighbor))

        return distances, predecessors

    def bellman_ford(self, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any], bool]:
        """Compute shortest paths using Bellman-Ford algorithm.

        Args:
            start: The starting vertex.

        Returns:
            A tuple of (distance, predecessor, has_negative_cycle).

        Raises:
            KeyError: If start vertex doesn't exist.
        """
        if start not in self.vertices:
            raise KeyError(f"Vertex {start} not found")

        distances = {v: math.inf for v in self.vertices}
        predecessors = {v: None for v in self.vertices}
        distances[start] = 0

        # Relax all edges V-1 times
        for _ in range(len(self.vertices) - 1):
            updated = False
            for (u, v), weight in self.weights.items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    updated = True
            if not updated:
                break

        # Check for negative cycles
        has_negative_cycle = False
        for (u, v), weight in self.weights.items():
            if distances[u] + weight < distances[v]:
                has_negative_cycle = True
                break

        return distances, predecessors, has_negative_cycle

    def prim_mst(self) -> Dict[Any, Any]:
        """Compute minimum spanning tree using Prim's algorithm.

        Returns:
            A dictionary of {vertex: parent} representing the MST.

        Raises:
            ValueError: If graph is disconnected.
        """
        if not self.vertices:
            return {}

        start = next(iter(self.vertices))
        mst = {v: None for v in self.vertices}
        key = {v: math.inf for v in self.vertices}
        key[start] = 0
        heap = [(0, start)]

        while heap:
            current_key, u = heapq.heappop(heap)
            for v in self.neighbors(u):
                weight = self.get_edge_weight(u, v)
                if v not in mst or weight < key[v]:
                    key[v] = weight
                    mst[v] = u
                    heapq.heappush(heap, (key[v], v))

        if any(v is None for v in mst.values()):
            raise ValueError("Graph is disconnected - cannot create MST")
        return mst

    def kruskal_mst(self) -> List[Tuple[Any, Any, float]]:
        """Compute minimum spanning tree using Kruskal's algorithm.

        Returns:
            A list of edges in the MST as (u, v, weight) tuples.

        Raises:
            ValueError: If graph is disconnected.
        """
        parent = {v: v for v in self.vertices}
        rank = {v: 0 for v in self.vertices}

        def find(u: Any) -> Any:
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u: Any, v: Any) -> None:
            root_u = find(u)
            root_v = find(v)
            if root_u == root_v:
                return
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            else:
                parent[root_u] = root_v
                if rank[root_u] == rank[root_v]:
                    rank[root_v] += 1

        edges = sorted(
            [(u, v, w) for (u, v), w in self.weights.items()],
            key=lambda x: x[2]
        )
        mst = []

        for u, v, w in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
                if len(mst) == len(self.vertices) - 1:
                    break

        if len(mst) != len(self.vertices) - 1:
            raise ValueError("Graph is disconnected - cannot create MST")
        return mst

    def floyd_warshall(self) -> Tuple[Dict[Any, Dict[Any, float]], Dict[Any, Dict[Any, Any]]]:
        """Compute all-pairs shortest paths using Floyd-Warshall algorithm.

        Returns:
            A tuple of (distance, next_vertex) matrices.
        """
        dist = {u: {v: math.inf for v in self.vertices} for u in self.vertices}
        next_vertex = {u: {v: None for v in self.vertices}
                       for u in self.vertices}

        # Initialize distances
        for u in self.vertices:
            dist[u][u] = 0
            for v in self.neighbors(u):
                dist[u][v] = self.get_edge_weight(u, v)
                next_vertex[u][v] = v

        # Main algorithm
        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]

        return dist, next_vertex

    def get_shortest_path(self, predecessors: Dict[Any, Any], target: Any) -> List[Any]:
        """Reconstruct shortest path from predecessors dictionary.

        Args:
            predecessors: Dictionary from Dijkstra/Bellman-Ford.
            target: The target vertex.

        Returns:
            A list of vertices in the shortest path.

        Raises:
            KeyError: If target vertex doesn't exist.
            ValueError: If no path exists.
        """
        if target not in self.vertices:
            raise KeyError(f"Vertex {target} not found")

        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessors.get(current)
            if current in path:  # Detect cycles
                raise ValueError("Negative cycle detected in path")

        if len(path) == 1 and path[0] == target and predecessors[target] is None:
            raise ValueError(f"No path to target vertex {target}")

        return path[::-1]

    def get_all_edges(self) -> List[Tuple[Any, Any, float]]:
        """Get all edges with their weights.

        Returns:
            A list of (u, v, weight) tuples.
        """
        return [(u, v, w) for (u, v), w in self.weights.items()]
