import logging
import logging.handlers
import os
import pandas as pd
from datetime import datetime# Logger configuration

logger = logging.getLogger(__name__)
LOG_LEVEL = "DEBUG"
LOG_FILE = "data_cleaning.log"

# Ensure the log file directory exists
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set log level
logger.setLevel(getattr(logging, LOG_LEVEL))

# Custom formatter with detailed information

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - data_injestion.py:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Rotating file handler (size-based rotation, max 5MB per file, keep 5 backups)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Timed rotating file handler (rotates daily, keeps 7 days of logs)
timed_file_handler = logging.handlers.TimedRotatingFileHandler(
    LOG_FILE,
    when='midnight',
    interval=1,
    backupCount=7
)
timed_file_handler.setLevel(logging.DEBUG)
timed_file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def read_dataset(url):
    """
    Reads a dataset from a specified URL into a pandas DataFrame.

    Args:
        url (str): The URL or file path to the dataset in CSV format.

    Returns:
        pandas.DataFrame: The loaded dataset as a DataFrame.

    Raises:
        Exception: Propagates any exception encountered while loading the dataset,
                with an error logged for debugging.
    """
    try:
        logger.info("Success! File loaded into a pandas dataframe")
        return pd.read_csv(url)
    except Exception as e:
        logger.error("Error while loading your dataset")
        raise e