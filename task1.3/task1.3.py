"""
Railway Route Planning System
Solves the Traveling Salesman Problem variant for railway cargo delivery
"""

import csv
import heapq
from itertools import permutations
from typing import Dict, List, Tuple, Set
import sys


class RailwayNetwork:
    """Class to represent and analyze the railway network"""
    
    def __init__(self, csv_file: str):
        """Initialize the railway network from CSV file"""
        self.graph: Dict[str, Dict[str, float]] = {}
        self.stations: Set[str] = set()
        self.load_network(csv_file)
    
    def load_network(self, csv_file: str):
        """Load railway network data from CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 3:
                       station1 = row[0].strip()
                    station2 = row[1].strip()
                        
                        # Get exact directional weights
                    weight_ab = float(row[2])
                        # If a return weight exists in col 4, use it. Otherwise, assume it's the same.
                    weight_ba = float(row[3]) if len(row) >= 4 else weight_ab
                        
                        # Add stations to set
                    self.stations.add(station1)
                    self.stations.add(station2)
                        
                        # Add DIRECTED edges (A->B has its own cost, B->A has its own cost)
                    if station1 not in self.graph:
                        self.graph[station1] = {}
                    if station2 not in self.graph:
                        self.graph[station2] = {}
                        
                    self.graph[station1][station2] = weight_ab
                    self.graph[station2][station1] = weight_ba
            
            print(f"Successfully loaded {len(self.stations)} stations from network data")
        except FileNotFoundError:
            print(f"Error: Could not find file {csv_file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading network data: {e}")
            sys.exit(1)
    
    def validate_station(self, station: str) -> bool:
        """Check if a station exists in the network"""
        return station in self.stations
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity score between two strings (0-1, higher is more similar)"""
        str1_lower = str1.lower()
        str2_lower = str2.lower()
        
        # Exact match
        if str1_lower == str2_lower:
            return 1.0
        
        # Contains match (higher score if contained)
        if str1_lower in str2_lower:
            return 0.9 - (len(str2_lower) - len(str1_lower)) / 100
        if str2_lower in str1_lower:
            return 0.85 - (len(str1_lower) - len(str2_lower)) / 100
        
        # Levenshtein-like similarity
        # Count matching characters in order
        matches = 0
        j = 0
        for char in str1_lower:
            if j < len(str2_lower):
                if char in str2_lower[j:]:
                    idx = str2_lower[j:].index(char)
                    matches += 1
                    j += idx + 1
        
        # Normalize by average length
        avg_len = (len(str1_lower) + len(str2_lower)) / 2
        return matches / avg_len if avg_len > 0 else 0
    
    def search_stations(self, query: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Search for stations similar to query, returns list of (station, score) tuples"""
        query_lower = query.lower()
        results = []
        
        for station in self.stations:
            score = self.calculate_similarity(query, station)
            # Also boost score if query words match station words
            query_words = set(query_lower.split())
            station_words = set(station.lower().split())
            word_overlap = len(query_words & station_words)
            if word_overlap > 0:
                score += word_overlap * 0.2
            
            results.append((station, score))
        
        # Sort by score (descending) and return top matches
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def prompt_station_selection(self, query: str, max_results: int = 10) -> str:
        """Prompt user to select from search results or try again"""
        results = self.search_stations(query, max_results)
        
        if not results:
            return ""
        
        print(f"\n Search results for '{query}':")
        print("-" * 70)
        
        # Display results
        for i, (station, score) in enumerate(results, 1):
            # Only show stations with reasonable similarity
            if score > 0.1 or i <= 5:  # Always show at least top 5
                print(f"  {i:2d}. {station}")
            else:
                break
        
        display_count = min(i, len(results))
        print("-" * 70)
        print(f"  0. None of these - try again")
        print()
        
        # Get selection
        while True:
            try:
                choice = input(f"Select a station (0-{display_count}): ").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    return ""  # User wants to try again
                elif 1 <= choice_num <= display_count:
                    selected = results[choice_num - 1][0]
                    print(f"✓ Selected: {selected}\n")
                    return selected
                else:
                    print(f"Please enter a number between 0 and {display_count}")
            except ValueError:
                print("Please enter a valid number")
            except (EOFError, KeyboardInterrupt):
                return ""
    
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


def main():
    """Main function to run the route planning system"""
    
    # Initialize the railway network
    csv_file = "./task1.3/activity1_3_railnetwork_data.csv"
    print(f"Loading railway network from {csv_file}...")
    network = RailwayNetwork(csv_file)
    
    # Interactive mode
    print("\n" + "="*70)
    print("RAILWAY ROUTE PLANNING SYSTEM")
    print("="*70)
    
    while True:
        print("\nOptions:")
        print("1. Plan a new route")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            print("\nEnter station names (must match names in the network)")
            
            # Validate start station
            start = None
            while True:
                if start is None:
                    start = input("Start station: ").strip()
                if network.validate_station(start):
                    print(f"✓ Valid station: {start}\n")
                    break
                else:
                    selected = network.prompt_station_selection(start)
                    if selected:
                        start = selected
                        break
                    else:
                        start = None  # Try again
            
            # Validate end station
            end = None
            while True:
                if end is None:
                    end = input("End station: ").strip()
                if network.validate_station(end):
                    print(f"✓ Valid station: {end}\n")
                    break
                else:
                    selected = network.prompt_station_selection(end)
                    if selected:
                        end = selected
                        break
                    else:
                        end = None  # Try again
            
            # Validate intermediate stations
            intermediates = []
            intermediates_str = input("Intermediate stations (comma-separated, or press Enter to skip): ").strip()
            if intermediates_str:
                temp_intermediates = [s.strip() for s in intermediates_str.split(',')]
                for station in temp_intermediates:
                    if network.validate_station(station):
                        # Check if station is same as start or end
                        if station == start:
                            print(f"Error: '{station}' is already the start station!")
                            print(f"   Intermediate stations must be different from start/end stations.")
                            print(f"   Skipping '{station}'...\n")
                            continue
                        if station == end:
                            print(f"Error: '{station}' is already the end station!")
                            print(f"   Intermediate stations must be different from start/end stations.")
                            print(f"   Skipping '{station}'...\n")
                            continue
                        # Check for duplicates in intermediate stations
                        if station in intermediates:
                            print(f"Error: '{station}' is already in intermediate stations!")
                            print(f"   Each station can only be visited once.")
                            print(f"   Skipping duplicate '{station}'...\n")
                            continue
                        
                        intermediates.append(station)
                        print(f"✓ Valid station: {station}")
                    else:
                        selected = network.prompt_station_selection(station)
                        if selected:
                            # Same checks for selected station
                            if selected == start:
                                print(f"Error: '{selected}' is already the start station!")
                                print(f"   Intermediate stations must be different from start/end stations.")
                                print(f"   Skipping '{selected}'...\n")
                                continue
                            if selected == end:
                                print(f"Error: '{selected}' is already the end station!")
                                print(f"   Intermediate stations must be different from start/end stations.")
                                print(f"   Skipping '{selected}'...\n")
                                continue
                            if selected in intermediates:
                                print(f"Error: '{selected}' is already in intermediate stations!")
                                print(f"   Each station can only be visited once.")
                                print(f"   Skipping duplicate '{selected}'...\n")
                                continue
                            
                            intermediates.append(selected)
                        else:
                            print(f"Skipping '{station}'...\n")
            
            cost, route = network.solve_tsp_variant(start, end, intermediates)
            
            if route:
                network.print_route_details(route, cost)
                save = input("\nSave route to file? (y/n): ").strip().lower()
                if save == 'y':
                    name = input("Enter filename (default: route_output): ").strip()
                    filename = name + ".txt" 
                    if not filename:
                        filename = "route_output.txt"
                    network.save_route_to_file(route, cost, filename)
            else:
                print("\nNo valid route found!")
        
        elif choice == "2":
            print("\nThank you for using the Railway Route Planning System!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
