import json
from graph import Graph
from typing import List

class AirportsGraphADT:
    def __init__(self):
        self.graph = Graph()
        self.edges = json.load(open('./constants/edges.json'))
        
        for from_airport, to_airport in self.edges:
            self.graph.add_edge(from_airport, to_airport)
    
    def find_all_paths(self, start: str, end: str) -> List[List[str]]:
        return self.graph.find_all_paths(start, end)
    
    def find_shortest_path(self, start: str, end: str) -> List[str]:
        return self.graph.find_shortest_path(start, end)
    
    def find_all_paths_with_cost(self, start: str, end: str) -> List[List[str]]:
        all_paths = self.find_all_paths(start, end)
        all_paths_with_cost = []
        for path in all_paths:
            cost = 0
            for i in range(len(path) - 1):
                cost += self.edges[(path[i], path[i+1])]
            all_paths_with_cost.append((path, cost))
        return all_paths_with_cost
            
if __name__ == "__main__":
    airports_graph_adt = AirportsGraphADT()
    start_airport = str(input("Enter the starting airport: "))
    result = airports_graph_adt.graph.calculate_min_additional_routes(start_airport)
    print(f"Minimum number of additional routes needed from {start_airport}: {result}")
