from fastapi import FastAPI
import logging
from models import Metrics

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

#Will be removed when DB is implemented
latest_metrics = None

@app.post('/metrics/')
async def metrics(metrics: Metrics):
    global latest_metrics
    logging.info(f'Metrics received: {metrics}')
    latest_metrics = metrics

@app.get('/latest_metrics')
async def latest_metrics():
    return latest_metrics