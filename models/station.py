from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class Station(BaseModel):
    id: str = Field(default_factory=generate_id)
    timestamp: str = Field(default_factory=generate_date)
    degree_c: float
    degree_f: float
    humidity: float
    ppm_mq135: float
    voltage_ldr: float
    presence: float
    device_id: str