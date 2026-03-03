from typing import List, Tuple, Set


class StationMatcher:
    """Class to handle fuzzy station name matching and interactive selection"""
    
    def __init__(self, stations: Set[str]):
        """Initialize with set of valid station names"""
        self.stations = stations
    
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