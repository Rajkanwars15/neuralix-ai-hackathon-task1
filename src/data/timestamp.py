import pandas as pd
import os


def read_sort_and_save_data(input_file_path, output_directory):
    # Define column names
    names = [
        'Date/Time',
        'LV ActivePower',
        'Wind Speed',
        'Theoretical_Power_Curve',
        'Wind Direction (deg)',
    ]

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path, sep=",", skiprows=1, names=names)

    # Convert the 'Date/Time' column to datetime objects
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    # Sort the DataFrame by the 'Date/Time' column
    df = df.sort_values(by='Date/Time')

    # Define the output file path
    output_file_path = os.path.join(output_directory, 'sorted_data.csv')

    # Save the sorted DataFrame to a CSV file
    df.to_csv(output_file_path, index=False)

    return output_file_path


# Define the directory paths
raw_data_file_path = '../../data/raw/T1.csv'
interim_data_directory = '../../data/interim'

# Call the function to read, sort, and save the data
saved_file_path = read_sort_and_save_data(raw_data_file_path, interim_data_directory)

print("Sorted data saved to:", saved_file_path)
