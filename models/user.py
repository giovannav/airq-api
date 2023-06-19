from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class User(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    surname: str
    email: str
    password: str
    created_at: str = Field(default_factory=generate_date)
    confirmed_email: bool = Field(default_factory=False)
    birthday: str
    station: list
    
class LoginRequest(BaseModel):
    email: str
    password: str