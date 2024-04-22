#I am using the github link for the logfile
#The results of this code will be saved to the file named log_monitor

import logging
import sys
import signal
import time
import re
import requests
from io import BytesIO

logging.basicConfig(filename='log_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def signal_handler(sig, frame):
    logging.info("Monitoring stopped by user.")
    sys.exit(0)

def monitor_log(log_file):
    logging.info(f"Monitoring log file: {log_file}")
    try:
        response = requests.get(log_file)
        if response.status_code == 200:
            log_content = response.text
            with BytesIO(log_content.encode()) as f:
                f.seek(0, 2)
                while True:
                    line = f.readline().decode()
                    if not line:
                        time.sleep(0.1)
                        continue
                    process_log_entry(line)
        else:
            logging.error(f"Failed to download log file: {log_file}")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Error occurred while downloading log file: {e}")
        sys.exit(1)

def process_log_entry(entry):
    error_pattern = re.compile(r'ERROR:')
    http_pattern = re.compile(r'HTTP/\d\.\d (\d{3})')

    if error_pattern.search(entry):
        logging.error(f"Error occurred: {entry.strip()}")
    if http_pattern.search(entry):
        status_code = http_pattern.search(entry).group(1)
        logging.info(f"HTTP Status Code: {status_code}")

def main():

    signal.signal(signal.SIGINT, signal_handler)
    log_file = 'https://raw.githubusercontent.com/aliraza89/Using-Python-to-Interact-with-the-Operating-System/main/Working%20with%20Log%20Files/Data/fishy.log'
    monitor_log(log_file)

if __name__ == "__main__":
    main()