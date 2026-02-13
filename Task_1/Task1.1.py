from data_process import data_read, data_clean, get_module_names
from utils import check_marks
from student_model import Student
filepath = "Task_1/data/activity1_1_marks.csv"
modules_names_data= "Task_1/data/cs modules.csv"


marks_data = data_read(filepath) # Call the data_read function to read the data from the specified CSV file.
module_names = data_read(modules_names_data) # Call the data_read function to read the module names from the specified CSV file.
if marks_data is not None and module_names is not None: # Check if both DataFrames were successfully read (not None).
    marks_data = data_clean(marks_data) # Call the data_clean function to clean the DataFrame
    module_names = data_clean(module_names) # Call the data_clean function to clean the module names DataFrame.
#print(marks_data)  Print the cleaned DataFrame to the console.
modules = get_module_names(module_names)

for index, row in marks_data.iterrows():
    student_id = row[0]
    # Create a new Student instance for this student
    student = Student(student_id, {}, {})
    # Add all modules for this student
    for i in range(1, len(row), 2):  # Use len(row) - 1 to prevent index out of range
        module_code = row[i]
        mark = row[i+1]
        #print("Student ID:", str(student_id), "Module Code:", str(module_code), "Mark:", str(mark))
        if module_code in modules:
            module_name = modules[module_code]
            student.add_module(module_name, module_code, mark)
    average = student.calculate_level_5_average() 
    print(f"Student ID: {student_id}, Average: {average[0]}, Total Credits: {average[1]}")
        
            #print("Student ID:", str(student_id), "Module Name:", str(module_name), "Mark:", str(mark))
            
            
        
        
#print (module_names)

