import pandas as pd
import os


def extract_and_save_monthly_data(input_file_path, output_directory):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Convert 'Date/Time' column to datetime objects
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])

    # Extract month from 'Date/Time'
    if 'Month' not in df:
        df['Month'] = df['Date/Time'].dt.month

    # Group by month and calculate sum of 'LV ActivePower'
    monthly_data = df.groupby('Month')['LV ActivePower'].sum()

    # Define the output file path
    output_file_path = os.path.join(output_directory, 'monthly_data.csv')

    # Save the monthly data to a CSV file
    monthly_data.to_csv(output_file_path, header=True)

    return output_file_path


# Define the directory paths
input_file_path = '../../data/interim/sorted_data.csv'
output_directory = '../../data/interim'

# Call the function to extract and save monthly data
saved_monthly_data_path = extract_and_save_monthly_data(input_file_path, output_directory)

print("Monthly data saved to:", saved_monthly_data_path)
