import sys
import os

# Add parent directory to sys.path so Python can find 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.data_logger import DataLogger

# Create logger with 5 sec interval and alpha=0.3 for EMA
logger = DataLogger(interval=1, alpha=0.1)

# Capture for 1 minute and save to CSV
logger.capture_data_csv(filename="sht30_log.csv", duration=200)
