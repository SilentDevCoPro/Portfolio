import time
import json
import psutil
import requests
import logging

def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'Error loading config file: {e}')
        exit(1)

def collect_metrics():
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
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        logging.info(f'Sent metrics to {url}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send metrics: {e}')

def main():
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