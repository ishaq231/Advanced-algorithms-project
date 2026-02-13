import pandas as pd

def data_read(data, ):
    try:
        data = pd.read_csv(data, header=None) # Read the CSV file into a pandas DataFrame without headers.
        return data
    except FileNotFoundError:
        print(f"Error: The file '{data}' was not found.")
        return None

def data_clean(data):
    # Function to clean the input pandas DataFrame.
    data = data.dropna() # Remove rows with any missing (NaN) values, modifying the DataFrame in place.
    data = data.drop_duplicates() # Remove duplicate rows, modifying the DataFrame in place.
    return data

def get_module_names(data):
    module_names = {}
    for index, row in data.iterrows():
        module_code = row[0]
        module_name = row[1]
        module_names[module_code] = module_name
    return module_names