from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key, Attr
import json
from datetime import datetime, timedelta
from decimal import Decimal

table = dynamodb.Table("station")

def create_station(station: dict):
    item = json.loads(json.dumps(station), parse_float=Decimal)
    try:
        table.put_item(Item=item)
        return item
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_station(id: str):
    try:
        response = table.scan(
            FilterExpression=Attr("device_id").eq(id)
        )
        items = response["Items"]
        
        # Convert timestamp values to datetime objects
        for item in items:
            original_timestamp = item["timestamp"]
            dt = datetime.strptime(original_timestamp, "%Y-%m-%d %H:%M:%S.%f")
            updated_dt = dt - timedelta(hours=3)
            updated_timestamp = updated_dt.strftime("%Y-%m-%d %H:%M:%S.%f")
            item["timestamp"] = updated_timestamp

        # Sort the items by timestamp
        sorted_items = sorted(items, key=lambda item: item["timestamp"], reverse=True)

        return sorted_items
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_stations():
    try:
        response = table.scan(
            AttributesToGet=["id", "timestamp", "degree_c", "degree_f", "humidity", "ppm_mq135", "voltage_ldr", "presence", "device_id"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)