import pandas as pd

def data_read(data):
    try:
        data = pd.read_csv(data) # Read the CSV file into a pandas DataFrame.
        return data
    except FileNotFoundError:
        print(f"Error: The file '{data}' was not found.")
        return None

def data_clean(data):
    # Function to clean the input pandas DataFrame.
    data = data.dropna() # Remove rows with any missing (NaN) values, modifying the DataFrame in place.
    data = data.drop_duplicates() # Remove duplicate rows, modifying the DataFrame in place.
    return data
filepath = './data/activity1_1_marks.csv'
class Student:
    def __init__(self,student_id,level_5_modules,level_6_modules):
        self.student_id = student_id
        self.level_5_modules = {}
        self.level_6_modules = {}
    def add_module(self,module,module_code,mark):
        module_code = module_code.split('-')
        credit = module_code[1]
        level = module_code[2]
        pass
    def calculate_level_5_average(): 
        pass
    def calculate_level_6_average():
        pass


marks_data = data_clean(filepath) # Call the data_clean function to read and clean the data from the specified CSV file.





