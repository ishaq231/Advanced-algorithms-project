import csv
import sys
from typing import Dict, Set


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