import json
from config import LOGGING_CONFIG
import logging

# Set up logging
logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def save_to_json(data, filename='output.json'):
    """Save extracted data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving data to {filename}: {e}")