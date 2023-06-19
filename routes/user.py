from fastapi import APIRouter, Request
from models.user import User, LoginRequest
from database.user import create_user, get_user, get_users, login, update_station, delete_station, update_user

routes_users = APIRouter()

@routes_users.get("/")
async def root():
    return {"message": "Hello World"}

@routes_users.post("/create", response_model=User)
async def create(user: User):
    return create_user(user.dict())

@routes_users.get("/get/{id}")
async def get_by_id(id: str):
    return get_user(id)

@routes_users.get("/all")
async def get_all():
    return get_users()

@routes_users.post("/login")
async def get_login(login_request:LoginRequest):
    return login(login_request.dict())

@routes_users.put("/update_station/{id}")
async def update_station_by_id(id: str, request: Request):
    station = await request.json()
    return update_station(id, station.get("station", []))

@routes_users.put("/delete_station/{user_id}")
async def delete_station_by_id(user_id: str):
    response = delete_station(user_id)
    return response

@routes_users.put("/update_user/{id}")
async def update_user_by_id(id: str, name:str = None, surname:str = None, password:str = None, birthday:str = None):
    response = update_user(id, name, surname, password, birthday)
    return response