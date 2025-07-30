from typing import Dict, List, Set, Optional, Any
from .graph import Graph

class DirectedGraph(Graph):
    """
    A directed graph implementation using adjacency lists.
    
    This class represents a directed graph where edges have a direction from
    one vertex to another. It supports weighted edges and provides common
    graph algorithms for directed graphs.
    
    Attributes:
        directed (bool): Always True for this class (used for compatibility with base Graph class)
        adjacency_list (Dict[Any, Dict[Any, Optional[float]]]): Adjacency list representation of the graph
    """
    
    def __init__(self, directed: bool = True):
        """
        Initialize a directed graph.
        
        Args:
            directed: Always True for this class (kept for compatibility with base Graph class)
        """
        super().__init__(directed=True)  # Force directed=True for this class
        
    def add_edge(self, v1: Any, v2: Any, weight: Optional[float] = None) -> None:
        """
        Add a directed edge from vertex v1 to vertex v2.
        
        Args:
            v1: The source vertex
            v2: The destination vertex
            weight: Optional weight for the edge (default: None)
            
        Raises:
            ValueError: If either vertex doesn't exist in the graph
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list:
            raise ValueError("Both vertices must exist in the graph")
            
        self.adjacency_list[v1][v2] = weight
        
    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Remove the directed edge from vertex v1 to vertex v2.
        
        Args:
            v1: The source vertex
            v2: The destination vertex
            
        Raises:
            ValueError: If the edge doesn't exist
        """
        if v1 not in self.adjacency_list or v2 not in self.adjacency_list[v1]:
            raise ValueError(f"Edge from {v1} to {v2} does not exist")
            
        del self.adjacency_list[v1][v2]
        
    def degree(self, vertex: Any) -> int:
        """
        Return the total degree (in-degree + out-degree) of the vertex.
        
        Args:
            vertex: The vertex to calculate degree for
            
        Returns:
            int: Total degree of the vertex
            
        Raises:
            ValueError: If the vertex doesn't exist
        """
        return self.in_degree(vertex) + self.out_degree(vertex)
        
    def in_degree(self, vertex: Any) -> int:
        """
        Return the in-degree of the vertex (number of incoming edges).
        
        Args:
            vertex: The vertex to calculate in-degree for
            
        Returns:
            int: In-degree of the vertex
            
        Raises:
            ValueError: If the vertex doesn't exist
        """
        if vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
            
        count = 0
        for v in self.adjacency_list:
            if vertex in self.adjacency_list[v]:
                count += 1
        return count
        
    def out_degree(self, vertex: Any) -> int:
        """
        Return the out-degree of the vertex (number of outgoing edges).
        
        Args:
            vertex: The vertex to calculate out-degree for
            
        Returns:
            int: Out-degree of the vertex
            
        Raises:
            ValueError: If the vertex doesn't exist
        """
        if vertex not in self.adjacency_list:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
            
        return len(self.adjacency_list[vertex])
        
    def transpose(self) -> 'DirectedGraph':
        """
        Return the transpose of the graph (all edges reversed).
        
        Returns:
            DirectedGraph: A new graph with all edges reversed
        """
        transposed = DirectedGraph()
        
        # Add all vertices
        for vertex in self.get_vertices():
            transposed.add_vertex(vertex)
            
        # Add reversed edges
        for v1 in self.adjacency_list:
            for v2 in self.adjacency_list[v1]:
                weight = self.adjacency_list[v1][v2]
                transposed.add_edge(v2, v1, weight)
                
        return transposed
        
    def strongly_connected_components(self) -> List[List[Any]]:
        """
        Find all strongly connected components using Kosaraju's algorithm.
        
        Returns:
            List[List[Any]]: A list of strongly connected components (each is a list of vertices)
        """
        # Step 1: Perform DFS on the original graph and record finish times
        visited = set()
        order = []
        
        def dfs(v):
            stack = [(v, False)]
            while stack:
                node, processed = stack.pop()
                if processed:
                    order.append(node)
                    continue
                if node in visited:
                    continue
                visited.add(node)
                stack.append((node, True))
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in visited:
                        stack.append((neighbor, False))
        
        for vertex in self.get_vertices():
            if vertex not in visited:
                dfs(vertex)
                
        # Step 2: Perform DFS on the transpose graph in reverse order of finish times
        transposed = self.transpose()
        visited = set()
        components = []
        
        while order:
            v = order.pop()
            if v not in visited:
                stack = [v]
                visited.add(v)
                component = []
                while stack:
                    node = stack.pop()
                    component.append(node)
                    for neighbor in transposed.adjacency_list[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            stack.append(neighbor)
                components.append(component)
                
        return components
        
    def topological_sort(self) -> List[Any]:
        """
        Perform topological sort using Kahn's algorithm.
        
        Returns:
            List[Any]: A topological ordering of vertices
            
        Raises:
            ValueError: If the graph contains a cycle
        """
        if self.is_cyclic():
            raise ValueError("Graph contains a cycle, topological sort not possible")
            
        # Calculate in-degrees
        in_degree = {v: 0 for v in self.get_vertices()}
        for v1 in self.adjacency_list:
            for v2 in self.adjacency_list[v1]:
                in_degree[v2] += 1
                
        # Initialize queue with vertices having 0 in-degree
        queue = [v for v in in_degree if in_degree[v] == 0]
        top_order = []
        
        while queue:
            v = queue.pop(0)
            top_order.append(v)
            
            for neighbor in self.adjacency_list[v]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        return top_order
        
    def is_cyclic(self) -> bool:
        """
        Check if the graph contains any cycles using DFS.
        
        Returns:
            bool: True if the graph contains a cycle, False otherwise
        """
        visited = set()
        recursion_stack = set()
        
        def is_cyclic_util(v):
            visited.add(v)
            recursion_stack.add(v)
            
            for neighbor in self.adjacency_list[v]:
                if neighbor not in visited:
                    if is_cyclic_util(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
                    
            recursion_stack.remove(v)
            return False
            
        for vertex in self.get_vertices():
            if vertex not in visited:
                if is_cyclic_util(vertex):
                    return True
                    
        return False