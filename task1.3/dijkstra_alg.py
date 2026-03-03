import heapq
from itertools import permutations
from typing import Dict, List, Tuple


class RouteOptimizer:
    """Class to handle route optimization using Dijkstra's algorithm and TSP solving"""
    
    def __init__(self, graph: Dict[str, Dict[str, float]], stations):
        """Initialize with the network graph and stations set"""
        self.graph = graph
        self.stations = stations
    
    def dijkstra(self, start: str, end: str) -> Tuple[float, List[str]]:
        """
        Find shortest path between two stations using Dijkstra's algorithm
        Returns: (cost, path)
        """
        if start not in self.graph or end not in self.graph:
            return float('inf'), []
        
        if start == end:
            return 0, [start]
        
        # Priority queue: (cost, current_station, path)
        pq = [(0, start, [start])]
        visited = set()
        
        while pq:
            cost, current, path = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == end:
                return cost, path
            
            # Explore neighbors
            for neighbor, edge_cost in self.graph[current].items():
                if neighbor not in visited:
                    new_cost = cost + edge_cost
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
        
        return float('inf'), []
    
    def build_distance_matrix(self, stations_to_visit: List[str]) -> Dict[Tuple[str, str], Tuple[float, List[str]]]:
        """
        Build distance matrix for an Asymmetric Directed Graph.
        Calculates exact paths for both directions independently.
        """
        distance_matrix = {}
        
        for i, station1 in enumerate(stations_to_visit):
            for station2 in stations_to_visit:
                # Skip if it's the exact same station
                if station1 == station2:
                    continue
                    
                # We must calculate Dijkstra specifically for this exact direction
                cost, path = self.dijkstra(station1, station2)
                distance_matrix[(station1, station2)] = (cost, path)
                
        return distance_matrix
    
    def solve_tsp_variant(self, start_station: str, end_station: str, 
                         intermediate_stations: List[str]) -> Tuple[float, List[str]]:
        """
        Solve TSP variant: visit all intermediate stations starting from start_station
        and ending at end_station
        
        Returns: (total_cost, complete_route)
        """
        # Validate stations
        all_stations = [start_station] + intermediate_stations + [end_station]
        for station in all_stations:
            if station not in self.stations:
                print(f"Error: Station '{station}' not found in network")
                return float('inf'), []
        
        # Build distance matrix for all required stations
        stations_to_visit = list(set([start_station, end_station] + intermediate_stations))
        print(f"\nCalculating shortest paths between all required stations...")
        distance_matrix = self.build_distance_matrix(stations_to_visit)
        
        # If start and end are the same, it's a classic TSP
        if start_station == end_station:
            return self._solve_tsp_cycle(start_station, intermediate_stations, distance_matrix)
        else:
            return self._solve_tsp_path(start_station, end_station, intermediate_stations, distance_matrix)
    
    def _solve_tsp_path(self, start: str, end: str, intermediates: List[str],
                       distance_matrix: Dict) -> Tuple[float, List[str]]:
        """
        Solve TSP variant where start != end
        Must visit all intermediate stations exactly once
        """
        if not intermediates:
            # Direct path from start to end
            cost, path = distance_matrix[(start, end)]
            return cost, path
        
        min_cost = float('inf')
        best_route = []
        
        # Try all permutations of intermediate stations
        print(f"Evaluating {len(list(permutations(intermediates)))} possible routes...")
        
        for perm in permutations(intermediates):
            # Calculate cost for this permutation
            current_cost = 0
            current_route = []
            
            # Start to first intermediate
            route_segment = [start] + list(perm)
            prev_station = start
            
            valid_route = True
            for next_station in perm:
                cost, path = distance_matrix[(prev_station, next_station)]
                if cost == float('inf'):
                    valid_route = False
                    break
                current_cost += cost
                if current_route:
                    current_route.extend(path[1:])  # Avoid duplicating station
                else:
                    current_route = path[:]
                prev_station = next_station
            
            if not valid_route:
                continue
            
            # Last intermediate to end
            cost, path = distance_matrix[(prev_station, end)]
            if cost == float('inf'):
                continue
            
            current_cost += cost
            current_route.extend(path[1:])  # Avoid duplicating station
            
            # Update best route if this is better
            if current_cost < min_cost:
                min_cost = current_cost
                best_route = current_route
        
        return min_cost, best_route
    
    def _solve_tsp_cycle(self, start: str, intermediates: List[str],
                        distance_matrix: Dict) -> Tuple[float, List[str]]:
        """
        Solve classic TSP where start == end (cycle)
        """
        if not intermediates:
            return 0, [start]
        
        min_cost = float('inf')
        best_route = []
        
        print(f"Evaluating {len(list(permutations(intermediates)))} possible routes (cycle)...")
        
        for perm in permutations(intermediates):
            current_cost = 0
            current_route = []
            
            # Start to first intermediate
            prev_station = start
            valid_route = True
            
            for next_station in perm:
                cost, path = distance_matrix[(prev_station, next_station)]
                if cost == float('inf'):
                    valid_route = False
                    break
                current_cost += cost
                if current_route:
                    current_route.extend(path[1:])
                else:
                    current_route = path[:]
                prev_station = next_station
            
            if not valid_route:
                continue
            
            # Return to start
            cost, path = distance_matrix[(prev_station, start)]
            if cost == float('inf'):
                continue
            
            current_cost += cost
            current_route.extend(path[1:])
            
            if current_cost < min_cost:
                min_cost = current_cost
                best_route = current_route
        
        return min_cost, best_route
    
    def print_route_details(self, route: List[str], total_cost: float):
        """Print detailed route information"""
        print("\n" + "="*70)
        print("OPTIMAL ROUTE FOUND")
        print("="*70)
        print(f"\nTotal Cost: {total_cost:.2f}")
        print(f"Number of stations in route: {len(route)}")
        print("\nDetailed Route:")
        print("-" * 70)
        
        for i, station in enumerate(route, 1):
            print(f"  {i:3d}. {station}")
        
        print("="*70)
    
    def save_route_to_file(self, route: List[str], total_cost: float, filename: str = "route_output.txt"):
        """Save route details to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("RAILWAY ROUTE PLANNING SYSTEM - OPTIMAL ROUTE\n")
                f.write("="*70 + "\n\n")
                f.write(f"Total Cost: {total_cost:.2f}\n")
                f.write(f"Number of stations in route: {len(route)}\n\n")
                f.write("Detailed Route:\n")
                f.write("-" * 70 + "\n")
                
                for i, station in enumerate(route, 1):
                    f.write(f"  {i:3d}. {station}\n")
                
                f.write("="*70 + "\n")
            
            print(f"\nRoute details saved to: {filename}")
        except Exception as e:
            print(f"Error saving route to file: {e}")