from data_process import data_read, data_clean, get_module_names
from utils import check_marks
from student_model import Student
import csv

filepath = "task1.1/data/activity1_1_marks.csv"
modules_names_data= "task1.1/data/cs modules.csv"


marks_data = data_read(filepath) # Call the data_read function to read the data from the specified CSV file.
if marks_data is not None: # Check if DataFrame was successfully read (not None).
    marks_data = data_clean(marks_data) # Call the data_clean function to clean the DataFrame
#print(marks_data)  Print the cleaned DataFrame to the console.
# Read module names directly using optimized csv method
modules = get_module_names(modules_names_data)
print("Data read and cleaned successfully. Module names extracted.")

# Open CSV file once and write incrementally
with open('task1.1/student_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Student ID', 'Level 5 Average', 'Level 6 Average', 'Final Grade', 'Final Mark', 'Modules Failed', 'level 5 Modules Used']
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
        
        writer.writerow({
            'Student ID': student_id,
            'Level 5 Average': f"{round(student.level_5_average, 1)}%",
            'Level 6 Average': f"{round(student.level_6_average, 1)}%",
            'Final Grade': check_marks(student.final_mark),
            'Final Mark': round(student.final_mark, 1),
            'Modules Failed': ", ".join(student.failed_modules) if student.has_fail else "None",
            'level 5 Modules Used': level_5_modules_str,
        })

print(f"\nResults saved to Task_1/student_results.csv")