import time
import json
import psutil
import requests
import logging

"""
This script monitors system resource usage (CPU, memory, and disk) and sends the metrics 
to a remote server at regular intervals. The configuration, including the remote server's URL 
and the interval, is loaded from a 'config.json' file. Metrics are collected using the psutil 
library and sent via HTTP POST requests. Errors and process events are logged for troubleshooting.
"""


def load_config():
    """
    Loads the application configuration from a 'config.json' file.
    If the file cannot be found or parsed, the process is terminated with an error log.

    Returns:
        dict: The loaded configuration from the JSON file.

    Logs:
        - Error details if the configuration file fails to load.
    """
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'Error loading config file: {e}')
        exit(1)


def collect_metrics():
    """
    Collects system resource metrics such as CPU, memory, and disk usage.
    Metrics are collected using the psutil library.

    Returns:
        dict: A dictionary containing the following metrics:
            - CPU usage percentage
            - Memory usage percentage, free memory, and total memory
            - Disk usage percentage, free disk space, and total disk space
            - UNIX timestamp of the data collection

    Logs:
        - The collected metrics for visibility and debugging purposes.
    """
    metrics = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_free': psutil.virtual_memory().free,
        'memory_total': psutil.virtual_memory().total,
        'disk_percent': psutil.disk_usage('/').percent,
        'disk_free': psutil.disk_usage('/').free,
        'disk_total': psutil.disk_usage('/').total,
        'timestamp': int(time.time())
    }
    logging.info(f'Metrics: {metrics}')
    return metrics


def send_metrics(url, data):
    """
    Sends the collected metrics to the specified URL via an HTTP POST request.
    If the request fails, an error is logged.

    Args:
        url (str): The URL of the remote collector to send metrics to.
        data (dict): The metrics data to be sent.

    Logs:
        - Success log on successful sending of metrics.
        - Error log if the HTTP request fails.
    """
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        logging.info(f'Sent metrics to {url}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send metrics: {e}')


def main():
    """
    Main function that configures logging, loads the configuration,
    and starts the monitoring loop to collect and send metrics at regular intervals.

    - It checks that a collector URL is specified in the configuration.
    - Runs indefinitely, collecting and sending metrics at the configured interval.

    Logs:
        - Errors if critical configuration values (like the collector URL) are missing.
        - General process information for easier debugging.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    config = load_config()
    interval = config.get('interval', 60)
    collector_url = config.get('collector_url')

    if not collector_url:
        logging.error("Collector URL not specified in agent/app/config.json")
        exit(1)

    while True:
        metrics = collect_metrics()
        send_metrics(collector_url, metrics)
        time.sleep(interval)


if __name__ == '__main__':
    main()
