import json
import os
from utils.logger import get_logger


# Persistence module for saving and loading JSON data when restarting the application. :)
logger = get_logger("Persistence")

def save_json(data, path):
    '''
    Saves the given data to a JSON file at the specified path.
    Args:
        data (dict): The data to be saved.
        path (str): The file path where the data should be saved.
    Returns:
        None
    '''
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved data to {path}")
    except Exception as e:
        logger.error(f"Error saving to {path}: {e}")

def load_json(path):
    '''
    Loads data from a JSON file at the specified path.
    Args:
        path (str): The file path from which to load the data.
    Returns:
        dict: The loaded data, or an empty dictionary if the file does not exist or an error occurs.
    '''
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded data from {path}")
        return data
    except FileNotFoundError:
        logger.warning(f"File not found: {path}")
        return {}
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return {}
