from fastapi import FastAPI
from database.db import create_tables
from routes.user import routes_users
from routes.device import routes_device
from routes.station import routes_station
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
app.include_router(routes_users, prefix="/user")
app.include_router(routes_device, prefix="/device")
app.include_router(routes_station, prefix="/station")
app.openapi()

create_tables()