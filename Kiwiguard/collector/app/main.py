from fastapi import FastAPI
from pydantic import BaseModel
import logging

class Metrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_free: float
    memory_total: float
    disk_percent: float
    disk_free: float
    disk_total: float
    timestamp: float

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


@app.post('/metrics/')
async def metrics(metrics: Metrics):
    logging.info(f'Metrics received: {metrics}')