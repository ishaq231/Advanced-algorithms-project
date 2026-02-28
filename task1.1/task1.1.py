import csv
import pandas as pd
filepath = "task1.1/data/activity1_1_marks.csv"
modules_names_data= "task1.1/data/cs modules.csv"

class Student:
    def __init__(self,student_id):
        self.student_id = student_id
        self.level_5_modules = {}
        self.level_5_average = 0
        self.level_6_modules = {}
        self.level_6_average = 0
        self.final_mark = 0
        self.has_fail = False  # Flag to track if any module is failed
        self.failed_modules = []  # List to store failed modules (if needed)
        self.level_5_modules_used = {}  # Modules actually used for Level 5 (best 100 credits)
        self.level_6_modules_used = {}  # Modules actually used for Level 6
    def add_module(self,module,module_code,mark):
        module_code_split = module_code.split('-')
        credit = module_code_split[1]
        year = module_code_split[2]
        
        # Check if this module is a fail
        if mark < 40:
            self.has_fail = True
            self.failed_modules.append(module)
        
        if year == '2':
            self.level_5_modules[module] = (int(credit),mark)
        elif year == '3':
            self.level_6_modules[module] = (int(credit),mark)
        #print(f"Level 5 Modules: {self.level_5_modules}")
        #print(f"Level 6 Modules: {self.level_6_modules}")
    def calculate_level_5_average(self):
        # Create a list of (module_name, mark, credit) tuples from all modules
        # Filter out invalid marks (marks should be between 0-100)
        modules_list = [(module, mark, credit) for module, (credit, mark) in self.level_5_modules.items() if 0 <= mark <= 100]
        
        # Sort by mark in descending order (highest marks first)
        modules_list.sort(reverse=True, key=lambda x: x[1])
        
        total_credits = 0
        weighted_sum = 0
        self.level_5_modules_used = {}  # Reset the modules used
        
        for module, mark, credit in modules_list:
            if total_credits >= 100:
                break
            
            # Check if adding this module would exceed 100 credits
            if total_credits + credit <= 100:
                # Add the full module
                total_credits += credit
                weighted_sum += mark * credit
                self.level_5_modules_used[module] = mark
            else:
                # Add partial credits to reach exactly 100
                remaining_credits = 100 - total_credits
                total_credits += remaining_credits
                weighted_sum += mark * remaining_credits
                self.level_5_modules_used[module] = mark
                break  # We've reached 100 credits
        
        self.level_5_average = weighted_sum / total_credits if total_credits > 0 else 0
        
    def calculate_level_6_average(self):
        # Direct calculation without intermediate list - more memory efficient
        total_credits = 0
        weighted_sum = 0
        self.level_6_modules_used = {}  # Reset the modules used
        
        for module, (credit, mark) in self.level_6_modules.items():
            if 0 <= mark <= 100:  # Exclude invalid marks
                total_credits += credit
                weighted_sum += mark * credit
                self.level_6_modules_used[module] = mark
        
        self.level_6_average = weighted_sum / total_credits if total_credits > 0 else 0
    
    def final_mark_calc(self):
        # If student failed any module, they don't get a degree
        if self.has_fail:
            self.final_mark = 0
            return 0
        
        final_mark = ((self.level_6_average * 3) + self.level_5_average)/4
        self.final_mark = final_mark 
        


def data_read(data):
    try:
        data = pd.read_csv(data, header=None) # Read the CSV file into a pandas DataFrame without headers.
        return data
    except FileNotFoundError:
        print(f"Error: The file '{data}' was not found.")
        return None

def data_clean(data):
    # Function to clean the input pandas DataFrame.
    # inplace operations are more memory efficient
    data.dropna(inplace=True) # Remove rows with any missing (NaN) values, modifying the DataFrame in place.
    data.drop_duplicates(inplace=True) # Remove duplicate rows, modifying the DataFrame in place.
    return data

def get_module_names(filepath):
    # More efficient: use csv module directly instead of pandas for small lookup table
    module_names = {}
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    module_names[row[0]] = row[1]
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    return module_names      

def check_marks(mark):
    """Return the grade classification based on the mark."""
    if mark >= 70:
        return "First Class"
    elif mark >= 60:
        return "(2:1) Upper Second Class"
    elif mark >= 50:
        return "(2:2) Lower Second Class"
    elif mark >= 40:
        return "Third Class"
    elif mark < 40:
        return "Fail"
    else:
        return "Invalid"



marks_data = data_read(filepath) # Call the data_read function to read the data from the specified CSV file.
if marks_data is not None: # Check if DataFrame was successfully read (not None).
    marks_data = data_clean(marks_data) # Call the data_clean function to clean the DataFrame
#print(marks_data)  Print the cleaned DataFrame to the console.
# Read module names directly using optimized csv method
modules = get_module_names(modules_names_data)
print("Data read and cleaned successfully. Module names extracted.")

# Open CSV file once and write incrementally
with open('task1.1/student_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Student ID', 'Level 5 Average', 'Level 6 Average', 'Final Grade', 'Final Mark', 'Modules Failed', 'level 5 Modules Used', 'level 6 Modules Used']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header once at the start
    writer.writeheader()
    
    # Process and write each student immediately
    # itertuples() is much faster than iterrows() - 100x+ performance improvement
    for row in marks_data.itertuples(index=False, name=None):
        student_id = row[0]
        # Create a new Student instance for this student
        student = Student(student_id)  
        # Add all modules for this student
        for i in range(1, len(row), 2):  # Use len(row) - 1 to prevent index out of range
            module_code = row[i]
            mark = row[i+1]
            #print("Student ID:", str(student_id), "Module Code:", str(module_code), "Mark:", str(mark))
            if module_code in modules:
                module_name = modules[module_code]
                student.add_module(module_name, module_code, mark)
        student.calculate_level_5_average() 
        #print(f"Student ID: {student_id}, Average: {average}, Total Credits: {credit}")
        student.calculate_level_6_average()
        #print(f"Student ID: {student_id}, Level 6 Average: {level_6_average}, Level 6 Total Credits: {level_6_credit}")
        student.final_mark_calc()
        
        # Write result immediately to file
        # Format modules used with their marks: "Module Name (Mark%)"
        level_5_modules_str = ", ".join([f"{mod} ({mark}%)" for mod, mark in student.level_5_modules_used.items()])
        level_6_modules_str = ", ".join([f"{mod} ({mark}%)" for mod, mark in student.level_6_modules_used.items()])
        
        writer.writerow({
            'Student ID': student_id,
            'Level 5 Average': f"{round(student.level_5_average, 1)}%",
            'Level 6 Average': f"{round(student.level_6_average, 1)}%",
            'Final Grade': check_marks(student.final_mark),
            'Final Mark': round(student.final_mark, 1),
            'Modules Failed': ", ".join(student.failed_modules) if student.has_fail else "None",
            'level 5 Modules Used': level_5_modules_str,
            'level 6 Modules Used': level_6_modules_str
        })

print(f"\nResults saved to Task_1/student_results.csv")