from collections import defaultdict, deque
from typing import List, Set

class Graph:
    def __init__(self):
        # using adjacacency list for graph representation
        self.adjacency_list = defaultdict(list)
        self.nodes = set()

    def add_edge(self, from_node: str, to_node: str) -> None:
        self.adjacency_list[from_node].append(to_node)
        self.nodes.add(from_node)
        self.nodes.add(to_node)

    def remove_edge(self, from_node: str, to_node: str) -> None:
        if from_node in self.adjacency_list and to_node in self.adjacency_list[from_node]:
            self.adjacency_list[from_node].remove(to_node)
            
            if not self.adjacency_list[from_node]:
                del self.adjacency_list[from_node]
            
            self.nodes.discard(from_node)
            self.nodes.discard(to_node)
                

    def find_all_paths(self, start: str, end: str) -> List[List[str]]:
        all_paths = []
        stack = [(start, [start])]

        while stack:
            node, path = stack.pop()
            if node == end:
                all_paths.append(path)
            else:
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in path:
                        stack.append((neighbor, path + [neighbor]))

        return all_paths
    
    def find_shortest_path(self, start: str, end: str) -> List[str]:
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in self.adjacency_list[node]:
                    queue.append((neighbor, path + [neighbor]))

        return None
    
    def find_reachable_nodes(self, start: str) -> Set[str]:
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited
    
    def find_strongly_connected_components(self) -> List[Set[str]]:
        def dfs_forward(node: str, visited: Set[str], stack: List[str]) -> None:
            visited.add(node)
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_forward(neighbor, visited, stack)
            stack.append(node)
        
        def dfs_reverse(node: str, visited: Set[str], component: Set[str]) -> None:
            visited.add(node)
            component.add(node)
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_reverse(neighbor, visited, component)
        
        visited = set()
        stack = []
        for node in self.nodes:
            if node not in visited:
                dfs_forward(node, visited, stack)
        
        reversed_graph = Graph()
        for node in self.nodes:
            for neighbor in self.adjacency_list[node]:
                reversed_graph.add_edge(neighbor, node)
        
        visited = set()
        components = []
        while stack:
            node = stack.pop()
            if node not in visited:
                component = set()
                dfs_reverse(node, visited, component)
                components.append(component)
        
        return components
    
    def calculate_min_additional_routes(self, start: str) -> int:
        reachable = self.find_reachable_nodes(start)
        sccs = self.find_strongly_connected_components()
        min_routes = 0,
        for scc in sccs:
            if start in scc or any(node in reachable for node in scc):
                continue
            has_incoming = False
            for node in scc:
                for source in self.nodes:
                    if (source not in scc and 
                        source in reachable and 
                        node in self.adjacency_list[source]):
                        has_incoming = True
                        break
                if has_incoming:
                    break
            
            if not has_incoming:
                min_routes += 1
        
        return min_routes