"""
Configuration file for MongoDB connection and project settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'startup_insights')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'startups')

# Data paths
DATA_DIR = 'data'
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
VISUALIZATIONS_DIR = 'visualizations'

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, VISUALIZATIONS_DIR]:
    os.makedirs(directory, exist_ok=True)
