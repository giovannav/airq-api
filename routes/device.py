from fastapi import APIRouter
from models.device import Device
from database.device import create_device, get_device, get_devices

routes_device = APIRouter()

@routes_device.get("/")
async def root():
    return {"message": "Hello World"}

@routes_device.post("/create", response_model=Device)
async def create(device: Device):
    return create_device(device.dict())

@routes_device.get("/get/{id}")
async def get_by_id(id: str):
    return get_device(id)

@routes_device.get("/all")
async def get_all():
    return get_devices()

# @routes_user.post("/delete")
# async def create(user: User):
#     return create_user(user.dict())

# @routes_user.post("/update")
# def create(user: User):
#     return create_user(user.dict())