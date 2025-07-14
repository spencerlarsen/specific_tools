import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse


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
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    # Define colors and labels for the universal legend
    colors = ['blue', 'red', 'green']
    labels = ['Actual (q_)', 'Desired (q_des_)', 'Commanded (q_cmd_)']
    legend_handles = []
    
    for i, generalized_coordinate in enumerate(columns):
        if i <= 6:
            for k, data_col in enumerate(generalized_coordinate):
                if k <= 2 and data_col in data.columns:  # Only plot if column exists
                    color = colors[k]
                    line = axes[i].plot(data[time_col], data[data_col], color=color, alpha=0.8)
                    
                    # Create legend handles only once (from first subplot)
                    if i == 0:
                        legend_handles.append(line[0])

            # Set custom subplot titles
            if i % 2 == 0:
                joint_idx = i // 2
                axes[i].set_title(f"Joint {joint_idx} (u)")
            else:
                joint_idx = i // 2
                axes[i].set_title(f"Joint {joint_idx} (v)")
            axes[i].set_xlabel(time_col)
            axes[i].set_ylabel("Radians")
            axes[i].grid(True, alpha=0.3)
    
    # Hide any unused subplots
    for j in range(len(columns), 6):
        fig.delaxes(axes[j])
    
    # Add universal legend at the top of the figure
    if legend_handles:
        fig.legend(legend_handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=3, fontsize=12)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Make room for the legend
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bellows Adaptive Joint Controller')
    parser.add_argument('-f',  '--file_path',         type=str,   default='/home/spencerlarsen/Documents/7.7 Track Data/trial_1.csv',    help='Path to the CSV file. Default is trial_1.csv.')
    args = parser.parse_args()

    file_path = args.file_path  # Replace with your CSV file path
    data = load_csv_data(file_path)

    if data is not None:
        summarize_data(data)

        # Plot up to 6 columns against time in a 2x3 subplot configuration
        time_col = 'time'
        columns_to_plot = []
        for i in range(6):
            columns = [f'q_{i}', f'q_des_{i}', f'q_cmd_{i}']
            columns_to_plot.append(columns)
        plot_columns_with_time(data, time_col, columns_to_plot)

    # Integrated average error calculation
    errors = []
    for i in range(6):
        true_values = data[f'q_{i}']  # Replace with your true column name
        actual_values = data[f'q_cmd_{i}']  # Replace with your actual column name
        error = integrated_average_error(true_values, actual_values)
        print(f"Integrated average error for generalized coordinate {i}: {error:.4f}")
        errors.append(error)

    print("\n                      Summary of Integrated Average Errors:")
    print(f"Integrated average error for all trials: {np.mean(errors):.4f}")

