from pydantic import BaseModel

class Metrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_free: float
    memory_total: float
    disk_percent: float
    disk_free: float
    disk_total: float
    timestamp: float
