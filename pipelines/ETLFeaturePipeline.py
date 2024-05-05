import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_SOURCE
from zenml import step, pipeline
from steps.a_load import load_data_from_csv
from steps.b_clean import clean_data
from steps.c_feature_engineering import FeatureEngineering
from steps.d_removing_outlier import remove_outliers
from error_logs import configure_logger
# Configure logger
logger = configure_logger()

@pipeline(name="ETLFeaturePipeline", enable_step_logs=True)
def run_pipeline():
    try:
        logger.info("==> Pipeline process has been started...")
        df = load_data_from_csv(DATA_SOURCE)
        df = clean_data(df)
        df = FeatureEngineering(df)
        df = remove_outliers(df)
        logger.info("==> Pipeline process has been done successfully!")
        return df
    except Exception as e:
        logger.error(f"==> Pipeline process has been failed: {e}")
        return None
         

if __name__ == "__main__":
    run_pipeline()
    # if df is not None:
    #     print(f"Data Table: \n {df.head()}\n")
    #     logger.info("==> Data has been loaded successfully..!\n")
    #     print(f"Data Shape: \n {df.shape}\n")
    #     # Save the processed data
    #     df.to_csv(PROCESSED_DATA_PATH, index=False)
    #     logger.info("==> Processed data has been saved successfully..!\n")
    # else:
    #     print("Error: Pipeline process has been failed.")


