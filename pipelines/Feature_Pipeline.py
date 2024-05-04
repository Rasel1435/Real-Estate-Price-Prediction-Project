import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_SOURCE, PROCESSED_DATA_PATH
from error_logs import configure_logger
# Configure logger
logger = configure_logger()

# Load the data from CSV file
def load_data_from_csv():
    try:
        logger.info("==> The Data Loading Starting..")
        df = pd.read_csv(DATA_SOURCE)
        df.groupby('area_type')['area_type'].agg('count')
        # Let's drop some unnecessary columns which are not very important for my model prediction
        df = df.drop(['area_type', 'availability', 'society', 'balcony'], axis='columns')
        logger.info("==> The Data has been loaded successfully..!")
        return df
    except FileNotFoundError as f:
        logger.error(f"File Not Found: {f}")
        return None
    
# Clean The Data

def clean_data(df):
    try:
        logger.info("==> The Data Cleaning Process has been Started...")
    # Drop rows with missing values
        df = df.dropna()

        # Extract BHK information from 'size' column
        df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

        # Define a function to convert square footage to numerical format
        def convert_sqft_to_num(x):
            tokens = x.split('-')
            if len(tokens) == 2:
                return (float(tokens[0]) + float(tokens[1])) / 2
            try:
                return float(x)
            except ValueError:
                return None

        # Apply the conversion function to the 'total_sqft' column
        df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
        logger.info("==> The data Cleaning Process has been done Successfully...!")
        return df
    
    except Exception as e:
        logger.error(f"==> Data Cleaning has been Failed: {e}")
        return None


def FeatureEngineering(df):
    try:
        logger.info("==> The Feature Engineering Process has been Started...")
        # Create a new feature to detect outliers
        df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']

        # Clean up location names by stripping extra spaces
        df['location'] = df['location'].apply(lambda x: x.strip())

        # Group locations by count and filter out those with less than or equal to 10 data points
        location_counts = df.groupby(
            'location')['location'].count().sort_values(ascending=False)
        locations_less_than_10 = location_counts[location_counts <= 10]

        # Replace locations with less than or equal to 10 data points with 'other'
        df['location'] = df['location'].apply(
            lambda x: 'other' if x in locations_less_than_10 else x)

        logger.info("==> The Feature Engineering Process has been done SuccessFully...!")
        return df
    except Exception as e:
        logger.error(f"==> Error: {e}")
        return None
    
def run_all_function():
    try:
        logger.info("==> Running all functions...")
        df = load_data_from_csv()
        df = clean_data(df)
        df = FeatureEngineering(df)
        logger.info("==> All Function has been Successfully..!")
        return df
    except Exception as e:
        logger.error(f"Error: {e}")
        return None




if __name__ == '__main__':
    df = run_all_function()
    if df is not None:
        print(f"Data Table: \n {df.head()}\n")
        logger.info("==> Data has been loaded successfully..!\n")
        print(f"Data Shape: \n {df.shape}\n")
        
        # Save the processed data
        df.to_csv(PROCESSED_DATA_PATH, index=False)
        logger.info("==> Processed data has been saved successfully..!\n")
    else:
        print("Error: Data loading failed. Please check logs for details.")