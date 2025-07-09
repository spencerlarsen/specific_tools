import pandas as pd
import numpy as np

def load_csv_data(file_path):
    """
    Load CSV data from the specified file path.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the loaded CSV data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return None
    
def summarize_data(data):
    """
    Summarize the DataFrame by providing basic statistics.
    
    Args:
        data (pd.DataFrame): The DataFrame to summarize.
        
    Returns:
        pd.DataFrame: DataFrame containing summary statistics.
    """
    if data is not None:
        summary = data.describe()
        print("Data Summary:")
        print(summary)
        return summary
    else:
        print("No data to summarize.")
        return None
    
def integrated_average_error(true, actual):
    """
    Calculate the integrated average error between true and actual values.
    
    Args:
        true (pd.Series): The true values.
        actual (pd.Series): The actual values.
        
    Returns:
        float: The integrated average error.
    """
    if len(true) != len(actual):
        raise ValueError("True and actual series must have the same length.")
    
    error = np.abs(true - actual)
    integrated_error = np.mean(error)
    return integrated_error

def main():
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    data = load_csv_data(file_path)
    
    if data is not None:
        summarize_data(data)
        
        # Example true and actual values for integrated average error calculation
        true_values = data['true_column']  # Replace with your true column name
        actual_values = data['actual_column']  # Replace with your actual column name
        
        error = integrated_average_error(true_values, actual_values)
        print(f"Integrated Average Error: {error}")