# DATA_SOURCE = 'online'
DATA_SOURCE = '../data/Bengaluru_House_Data.csv'
PROCESSED_DATA_PATH = '../data/Final_Pipelines_Data.csv'
FEATURE_GROUP_NAME = 'house_price_prediction'
FEATURE_GROUP_DESCRIPTION = "Real Estate House Price Prediction"
FEATURE_DESCRIPTIONS = [
    {"name": "Location", "description": "Total Location will be here it's str type"},
    {"name": "total_sqft", "description": "Total squree feet will be here"},
    {"name": "bhk", "description": "Type of Room"},
    {"name": "bath", "description": "Total bathrooms"},
    {"name": "price", "description": "Price will be here"},
]

TABLE_NAME = 'house-price-prediction'
# AWS credentials
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
MODEL_NAME = 'house-price-prediction'
DOCKER = 'cddad79d40d780e360cec50b02914b5dafb9d3a208d7b063e5feaa508c2bff82'