# Advanced Algorithms Project

A collection of algorithm implementations showcasing various optimization techniques, data processing, graph algorithms, and parallel computing.

## Table of Contents
- [Overview](#overview)
- [Task 1.1: Student Grade Calculator](#task-11-student-grade-calculator)
- [Task 1.2: Password Generator](#task-12-password-generator)
- [Task 1.3: Railway Route Planning System](#task-13-railway-route-planning-system)
- [Task 1.4: Parallel Face Recognition](#task-14-parallel-face-recognition)
- [Installation](#installation)
- [Usage](#usage)

---

## Overview

This project contains four distinct algorithmic implementations, each demonstrating different computer science concepts:

1. **Data Processing & Object-Oriented Design** - Student grade calculator
2. **Backtracking & Constraint Satisfaction** - Password generation
3. **Graph Algorithms & TSP Optimization** - Railway route planning
4. **Parallel Processing & Computer Vision** - Face recognition system

---

## Task 1.1: Student Grade Calculator

### Description
A comprehensive student grading system that processes CSV data to calculate final grades based on UK university classification standards.

### Features
- **Data Processing**: Efficient CSV reading and cleaning using pandas
- **Module Management**: Handles Level 5 (Year 2) and Level 6 (Year 3) modules
- **Credit Optimization**: Automatically selects best 100 credits from Level 5 modules
- **Grade Classification**: Implements UK degree classification system
  - First Class (70%+)
  - Upper Second Class / 2:1 (60-69%)
  - Lower Second Class / 2:2 (50-59%)
  - Third Class (40-49%)
  - Fail (<40%)

### Algorithm Details
- **Level 5 Average**: Selects top 100 credits by marks (optimized selection)
- **Level 6 Average**: Uses all Level 6 modules
- **Final Mark Calculation**: `(Level 6 Average × 3 + Level 5 Average) / 4`
- **Performance Optimizations**:
  - Uses `itertuples()` instead of `iterrows()` (100x+ faster)
  - Incremental CSV writing to minimize memory usage
  - Direct dictionary lookup for module names

### Files
- [task1.1.py](task1.1/task1.1.py) - Main execution script
- [student_model.py](task1.1/student_model.py) - Student class with grade calculation logic
- [data_process.py](task1.1/data_process.py) - Data loading and cleaning utilities
- [utils.py](task1.1/utils.py) - Helper functions for grade classification
- [student_results.csv](task1.1/student_results.csv) - Output file with calculated results

### Input Data
- `activity1_1_marks.csv` - Student marks data
- `cs modules.csv` - Module code to name mappings

### Output Format
```csv
Student ID, Level 5 Average, Level 6 Average, Final Grade, Final Mark, Modules Failed, level 5 Modules Used, level 6 Modules Used
```

---

## Task 1.2: Password Generator

### Description
A recursive password generator that creates passwords matching specific security constraints.

### Features
- **Constraint-Based Generation**: Passwords must contain:
  - At least 1 uppercase letter (max 2)
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character (max 2)
  - Must start with a letter
- **Backtracking Algorithm**: Efficiently prunes invalid branches
- **Buffered I/O**: Uses buffer (10,000 passwords) for optimized file writing
- **Customizable Length**: User-specified password length

### Algorithm Details
- **Type**: Recursive backtracking with constraint checking
- **Pruning**: Early termination when constraints violated (caps > 2, special > 2)
- **Character Sets**:
  - Uppercase: A, B, C, D, E
  - Lowercase: a, b, c, d, e
  - Numbers: 1, 2, 3, 4, 5
  - Special: $, &, %

### Performance Optimizations
- Set-based character lookups for O(1) membership testing
- Buffer flushing to reduce I/O operations
- Early pruning to avoid unnecessary recursion

### Files
- [Pasword_cracker.py](task1.2/Pasword_cracker.py) - Password generation script
- [possible_passwords.txt](task1.2/possible_passwords.txt) - Generated passwords output

### Usage Example
```
Enter the length of the password to generate: 5
Passwords added to file: 2400 out of 537824 possible combinations.
```

---

## Task 1.3: Railway Route Planning System

### Description
An advanced graph-based route planning system that solves a variant of the Traveling Salesman Problem (TSP) for railway cargo delivery.

### Features
- **Dijkstra's Algorithm**: Finds shortest paths between stations
- **TSP Solver**: Optimizes routes through multiple stations
- **Interactive Station Search**: Fuzzy matching with similarity scoring
- **Directed Graph Support**: Handles asymmetric edge weights (different costs for A→B vs B→A)
- **Route Validation**: Ensures all stations are visited exactly once

### Algorithm Details

#### 1. Dijkstra's Algorithm
- **Purpose**: Find shortest path between two stations
- **Time Complexity**: O((V + E) log V) with priority queue
- **Implementation**: Uses `heapq` for efficient priority queue

#### 2. TSP Variant Solver
- **Problem Type**: 
  - **Path TSP**: Start ≠ End (visit all intermediate stations)
  - **Cycle TSP**: Start = End (return to starting point)
- **Approach**: Brute force with permutations for small problem sizes
- **Time Complexity**: O(n! × E log V) where n = number of intermediate stations

#### 3. String Similarity Search
- Custom algorithm for fuzzy station name matching
- Features:
  - Exact match detection
  - Substring matching with length penalties
  - Sequential character matching (Levenshtein-like)
  - Word overlap boosting
- Returns top 10 matches with similarity scores

### Features in Detail

#### Distance Matrix Building
- Precomputes shortest paths between all required stations
- Handles directed graphs (A→B ≠ B→A)
- Caches results to avoid redundant calculations

#### Interactive User Interface
- Station name search with suggestions
- Input validation and error handling
- Progress indicators for long computations
- Route export to text file

### Files
- [task1.3.py](task1.3/task1.3.py) - Complete railway routing system
- [activity1_3_railnetwork_data.csv](task1.3/activity1_3_railnetwork_data.csv) - Network data

### Data Format
CSV format: `Station1, Station2, Cost_AB, Cost_BA`

### Usage Flow
1. Load railway network from CSV
2. Enter start station (with fuzzy search assistance)
3. Enter end station
4. Enter intermediate stations (comma-separated, optional)
5. System calculates optimal route
6. Option to save route to file

### Example Output
```
OPTIMAL ROUTE FOUND
======================================================================
Total Cost: 245.80
Number of stations in route: 8
Detailed Route:
----------------------------------------------------------------------
    1. London Kings Cross
    2. Birmingham New Street
    3. Manchester Piccadilly
    ...
======================================================================
```

---

## Task 1.4: Parallel Face Recognition

### Description
A high-performance face recognition system using parallel processing to scan large image datasets efficiently.

### Features
- **Parallel Processing**: Uses `ProcessPoolExecutor` for multi-core utilization
- **Optimized Face Detection**: Multiple optimizations for speed
  - Pre-detection of face locations before encoding
  - Small model for faster landmark detection
  - No upsampling for speed (upsample_num_times=0)
- **Early Termination**: Stops scanning when match is found
- **Visual Output**: Displays matched face with bounding box using OpenCV
- **Robust Error Handling**: Handles corrupted images gracefully

### Algorithm Details

#### Face Recognition Pipeline
1. **Load Known Face**: Extract encoding from reference image
2. **Parallel Scanning**: Distribute images across CPU cores
3. **Per-Image Processing**:
   - Load image
   - Detect face locations (optimized)
   - Compute face encodings (small model)
   - Compare with known encoding
4. **Match Detection**: Return first match and cancel remaining tasks
5. **Display Result**: Show matched image with bounding box

### Performance Optimizations

#### 1. Parallel Processing
- Uses all available CPU cores
- `ProcessPoolExecutor` for true parallelism (bypasses GIL)
- `as_completed()` for immediate result processing

#### 2. Face Detection Optimizations
```python
# Optimization 1: No upsampling (faster, slightly less accurate)
face_locations = face_recognition.face_locations(unknown_image, upsample_num_times=0)

# Optimization 2: Use small model (faster than default 68-point model)
unknown_encodings = face_recognition.face_encodings(
    unknown_image, 
    known_face_locations=face_locations, 
    model="small"
)
```

#### 3. Early Termination
- Cancels all pending tasks when match found
- Saves computation time on large datasets

#### 4. File Filtering
- Only processes `.jpg` files
- Skips system files (e.g., `.DS_Store`)

### Dependencies
- `face_recognition` - Face detection and recognition
- `cv2` (OpenCV) - Image display and drawing
- `concurrent.futures` - Parallel processing
- `dlib` - Required backend for face_recognition

### Files
- [activity1_4_serial.py](task1.4/activity1_4_serial.py) - Main parallel face recognition script
- `known_man.jpg` - Reference face image (not in repo)
- `imageset/` - Folder containing images to search

### Installation Note
Installing `face_recognition` may require pre-compiled `dlib` wheel on Windows:
```bash
# Download from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x
pip install dlib-20.0.99-cp313-cp313-win_amd64.whl
pip install face_recognition
```

### Usage
```python
python task1.4/activity1_4_serial.py
```

### Output Example
```
Starting parallel scan of 150 images...
Match found! in person_042.jpg
Total time: 2.34 seconds
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Advanced-algorithms-project
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Install dependencies**

For Task 1.1:
```bash
pip install pandas
```

For Task 1.4:
```bash
# On Windows, install dlib wheel first
pip install dlib-20.0.99-cp313-cp313-win_amd64.whl

# Then install face_recognition and opencv
pip install face_recognition opencv-python
```

---

## Usage

### Task 1.1: Student Grade Calculator
```bash
cd task1.1
python task1.1.py
```
Output will be saved to `student_results.csv`

### Task 1.2: Password Generator
```bash
cd task1.2
python Pasword_cracker.py
```
Follow the prompt to enter desired password length.

### Task 1.3: Railway Route Planning
```bash
cd task1.3
python task1.3.py
```
Follow the interactive prompts to plan routes.

### Task 1.4: Face Recognition
```bash
cd task1.4
python activity1_4_serial.py
```
Ensure `known_man.jpg` exists and `imageset/` contains images to search.

---

## Project Structure
```
Advanced-algorithms-project/
├── task1.1/                    # Student Grade Calculator
│   ├── task1.1.py             # Main script
│   ├── student_model.py       # Student class
│   ├── data_process.py        # Data utilities
│   ├── utils.py               # Helper functions
│   ├── student_results.csv    # Output
│   └── data/                  # Input CSV files
├── task1.2/                    # Password Generator
│   ├── Pasword_cracker.py     # Main script
│   └── possible_passwords.txt # Output
├── task1.3/                    # Railway Route Planner
│   ├── task1.3.py             # Main script
│   └── activity1_3_railnetwork_data.csv
├── task1.4/                    # Face Recognition
│   ├── activity1_4_serial.py  # Main script
│   └── imageset/              # Image dataset
├── LICENSE
└── README.md
```

---

## Key Algorithms & Techniques

### 1. Data Processing & Optimization
- Pandas DataFrame operations
- Efficient CSV handling
- Memory-conscious iterative processing
- Dictionary-based lookups

### 2. Backtracking & Recursion
- Constraint satisfaction problems
- Branch pruning for efficiency
- Recursive generation with early termination

### 3. Graph Algorithms
- **Dijkstra's Algorithm**: Single-source shortest path
- **Traveling Salesman Problem**: Route optimization
- Directed graph handling with asymmetric weights
- Distance matrix precomputation

### 4. Parallel Computing
- Multi-process parallelism
- Work distribution across CPU cores
- Early termination strategies
- Efficient result aggregation

### 5. String Matching
- Fuzzy search algorithms
- Similarity scoring
- Levenshtein-like distance calculation

---

## Performance Characteristics

| Task | Algorithm | Time Complexity | Space Complexity | Optimization Techniques |
|------|-----------|-----------------|------------------|------------------------|
| 1.1 | Student Grading | O(n × m) | O(n) | itertuples, buffered I/O |
| 1.2 | Password Gen | O(k^n) | O(n) | Early pruning, buffering |
| 1.3 | TSP Routing | O(n! × E log V) | O(V²) | Dijkstra + permutations |
| 1.4 | Face Recognition | O(n/p) | O(n) | Parallel processing, early exit |

Where:
- n = number of items/students/stations/images
- m = number of modules per student
- k = character set size
- V = vertices/stations
- E = edges/connections
- p = number of CPU cores

---

## Future Enhancements

### Task 1.1
- [ ] Add visualization of grade distributions
- [ ] Implement grade boundaries adjustment
- [ ] Support for different credit systems

### Task 1.2
- [ ] Add password strength validation
- [ ] Support custom character sets
- [ ] Implement iterative version for better memory usage

### Task 1.3
- [ ] Implement branch-and-bound for larger TSP instances
- [ ] Add genetic algorithm for approximate solutions
- [ ] Support for time-dependent edge weights
- [ ] Route visualization on map

### Task 1.4
- [ ] Support for multiple known faces
- [ ] Real-time video face recognition
- [ ] GPU acceleration support
- [ ] Face clustering and organization

---

## License

See [LICENSE](LICENSE) file for details.

---

## Author

Ishaq Modassir Mushtaq  
University Year 2 Individual Project  
Advanced Algorithms Module

---

## Acknowledgments

- Face recognition library by Adam Geitgey
- UK university grading system standards
- Graph algorithm implementations from classic CS literature