import pandas as pd
import csv

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