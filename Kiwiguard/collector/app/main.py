from fastapi import FastAPI
import logging
from models import Metrics

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

@app.post('/metrics/')
async def metrics(metrics: Metrics):
    logging.info(f'Metrics received: {metrics}')