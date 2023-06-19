from fastapi import APIRouter
from models.station import Station
from database.station import create_station, get_station, get_stations

routes_station= APIRouter()

@routes_station.get("/")
async def root():
    return {"message": "Hello World"}

@routes_station.post("/create", response_model=Station)
async def create(station: Station):
    return create_station(station.dict())

@routes_station.get("/get/{device_id}")
async def get_by_id(device_id: str):
    return get_station(device_id)

@routes_station.get("/all")
async def get_all():
    return get_stations()
