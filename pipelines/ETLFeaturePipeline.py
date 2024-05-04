import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from config import DATA_SOURCE, PROCESSED_DATA_PATH
from steps import a_load
from steps import b_clean
from steps import c_feature_engineering
from steps import d_removing_outlier
from error_logs import configure_logger
# Configure logger
logger = configure_logger()

def run_pipeline():
    try:
        logger.info("==> Pipeline process has been started...")
        df = a_load.load_data_from_csv(DATA_SOURCE)
        df = b_clean.clean_data(df)
        df = c_feature_engineering.FeatureEngineering(df)
        df = d_removing_outlier.remove_outliers(df)
        logger.info("==> Pipeline process has been done successfully!")
        return df
    except Exception as e:
        logger.error(f"==> Pipeline process has been failed: {e}")
        return None
         

if __name__ == "__main__":
    df = run_pipeline()
    if df is not None:
        print(f"Data Table: \n {df.head()}\n")
        logger.info("==> Data has been loaded successfully..!\n")
        print(f"Data Shape: \n {df.shape}\n")
        # Save the processed data
        df.to_csv(PROCESSED_DATA_PATH, index=False)
        logger.info("==> Processed data has been saved successfully..!\n")
    else:
        print("Error: Pipeline process has been failed.")


