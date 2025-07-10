import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def plot_columns_with_time(data, time_col, columns):
    """
    Plot specified columns against the time column in a 2x3 subplot configuration.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        time_col (str): The name of the time column.
        columns (list): List of list of column names to plot (up to 6).
    """
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()
    for i, generalized_coordinate in enumerate(columns):
        if i <= 6:
            for k, data_col in enumerate(generalized_coordinate):
                if k <= 3:
                    axes[i].plot(data[time_col], data[data_col])

            axes[i].set_title(f"{generalized_coordinate[1]}")
            axes[i].set_xlabel(time_col)
            axes[i].set_ylabel("Radians")
    # Hide any unused subplots
    for j in range(len(columns), 6):
        fig.delaxes(axes[j])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage

    file_path = r'..\7.7 Track Data\trial_1.csv'  # Replace with your CSV file path
    data = load_csv_data(file_path)

    if data is not None:
        summarize_data(data)

        # Plot up to 6 columns against time in a 2x3 subplot configuration
        time_col = 'time'
        columns_to_plot = []
        for i in range(5):
            columns = [f'q_{i}', f'q_des_{i}', f'q_cmd_{i}']
            columns_to_plot.append(columns)
        plot_columns_with_time(data, time_col, columns_to_plot)

        # # Example true and actual values for integrated average error calculation
        # true_values = data['true_column']  # Replace with your true column name
        # actual_values = data['actual_column']  # Replace with your actual column name
