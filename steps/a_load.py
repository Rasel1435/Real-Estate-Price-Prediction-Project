import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenml import step
from typing import Union

from config import DATA_SOURCE, PROCESSED_DATA_PATH
from error_logs import configure_logger
# Configure logger
logger = configure_logger()

# Load the data from CSV file
@step(name="Load Data", enable_step_logs=True, enable_artifact_metadata=True)
def load_data_from_csv() -> Union[pd.DataFrame, None]:
    try:
        logger.info("==> The Data Loading Starting...")
        df = pd.read_csv(DATA_SOURCE)
        df.groupby('area_type')['area_type'].agg('count')
        # Let's drop some unnecessary columns which are not very important for my model prediction
        df = df.drop(['area_type', 'availability', 'society', 'balcony'], axis='columns')
        logger.info("==> The Data has been loaded successfully...!")
        return df
    except FileNotFoundError as f:
        logger.error(f"File Not Found: {f}")
        return None
    
    
    

# if __name__ == '__main__':
#     df = load_data_from_csv()
#     df.to_csv(PROCESSED_DATA_PATH, index=False)