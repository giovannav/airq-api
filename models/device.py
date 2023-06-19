from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class Device(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str