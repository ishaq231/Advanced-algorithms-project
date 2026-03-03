"""
Railway Route Planning System
Solves the Traveling Salesman Problem variant for railway cargo delivery
"""

from graph_model import RailwayNetwork
from string_matcher import StationMatcher
from dijkstra_alg import RouteOptimizer


def main():
    """Main function to run the route planning system"""
    
    # Initialize the railway network
    csv_file = "./task1.3/data/activity1_3_railnetwork_data.csv"
    print(f"Loading railway network from {csv_file}...")
    network = RailwayNetwork(csv_file)
    
    # Initialize the station matcher and route optimizer
    matcher = StationMatcher(network.stations)
    optimizer = RouteOptimizer(network.graph, network.stations)
    
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
                    print(f"\u2713 Valid station: {start}\n")
                    break
                else:
                    selected = matcher.prompt_station_selection(start)
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
                    print(f"\u2713 Valid station: {end}\n")
                    break
                else:
                    selected = matcher.prompt_station_selection(end)
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
                        print(f"\u2713 Valid station: {station}")
                    else:
                        selected = matcher.prompt_station_selection(station)
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
            
            cost, route = optimizer.solve_tsp_variant(start, end, intermediates)
            
            if route:
                optimizer.print_route_details(route, cost)
                save = input("\nSave route to file? (y/n): ").strip().lower()
                if save == 'y':
                    name = input("Enter filename (default: route_output): ").strip()
                    filename = name + ".txt" 
                    if not filename:
                        filename = "route_output.txt"
                    optimizer.save_route_to_file(route, cost, filename)
            else:
                print("\nNo valid route found!")
        
        elif choice == "2":
            print("\nThank you for using the Railway Route Planning System!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()