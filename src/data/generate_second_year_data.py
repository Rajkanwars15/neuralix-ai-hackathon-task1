import numpy as np
import pandas as pd
import os


def generate_and_save_second_year_data(monthly_data_file_path, output_directory):
    # Load monthly data
    monthly_data = pd.read_csv(monthly_data_file_path, index_col='Month')

    # Generate noise
    np.random.seed(42)
    noise = np.random.normal(0, 10000000, size=monthly_data.shape[0])

    # Generate second year data
    second_year_data = monthly_data['LV ActivePower'] + noise

    # Calculate differences
    differences = second_year_data - monthly_data['LV ActivePower']

    # Create DataFrame for second year data
    second_year_df = pd.DataFrame(
        {'Month': monthly_data.index, 'Second Year Data': second_year_data, 'Differences': differences})

    # Define the output file path
    output_file_path = os.path.join(output_directory, 'second_year_data.csv')

    # Save the second year data to a CSV file
    second_year_df.to_csv(output_file_path, index=False)

    return output_file_path


# Define the directory paths
monthly_data_file_path = '../../data/interim/monthly_data.csv'
output_directory = '../../data/interim'

# Call the function to generate and save second year data
saved_second_year_data_path = generate_and_save_second_year_data(monthly_data_file_path, output_directory)

print("Second year data saved to:", saved_second_year_data_path)
