import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zenml import step
from typing import Union
from config import PROCESSED_DATA_PATH, DATA_SOURCE

from error_logs import configure_logger
# Configure logger
logger = configure_logger()

@step(name="Remove Outliers", enable_step_logs=True, enable_artifact_metadata=True)
def remove_outliers(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    try:
        logger.info("==> Removing outlier Function has been Started...")
        
        # Remove outliers based on total square feet per bedroom
        df = df[~(df.total_sqft/df.bhk < 300)]
        
        # Remove outliers based on price per square foot
        def remove_pps_outliers(subdf):
            m = np.mean(subdf.price_per_sqft)
            st = np.std(subdf.price_per_sqft)
            return subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        
        df = df.groupby('location', group_keys=False).apply(remove_pps_outliers)
        
        # Remove outliers based on bathroom count
        def remove_bath_outliers(subdf):
            return subdf[subdf.bath <= subdf.bhk + 2]
        
        df = df.groupby('location', group_keys=False).apply(remove_bath_outliers)
        
        # Drop unnecessary columns
        df = df.drop(['size', 'price_per_sqft'], axis='columns')
        
        logger.info("==> Removing outlier Function has been done Successfully...!")
        return df
 
    except Exception as e:
        logger.error(f"==> Error: Removing outlier Function has been failed. Error: {e}")
        return None


# if __name__ == "__main__":
#     df = pd.read_csv(r'C:/Users/SRA/Desktop/Real-Estate-Price-Prediction-Project/data/Final_Pipelines_Data.csv')
#     df = remove_outliers(df)
#     df.to_csv(PROCESSED_DATA_PATH, index=False)