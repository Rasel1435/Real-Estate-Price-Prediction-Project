import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zenml import step
from typing import Union
from config import PROCESSED_DATA_PATH, DATA_SOURCE

from error_logs import configure_logger
# Configure logger
logger = configure_logger()


# Clean The Data
@step(name="Clean Data", enable_step_logs=True, enable_artifact_metadata=True)
def clean_data(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    try:
        logger.info("==> The data Cleaning Process has been Started...")
    # Drop rows with missing values
        df = df.dropna().copy()

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
        logger.error(f"==> The Data Cleaning has been Failed: {e}")
        return None


# if __name__ == "__main__":
#     df = pd.read_csv(r'C:/Users/SRA/Desktop/Real-Estate-Price-Prediction-Project/data/Final_Pipelines_Data.csv')
#     df = clean_data(df)
#     df.to_csv(PROCESSED_DATA_PATH, index=False)