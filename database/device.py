from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("device")

def create_device(user: dict):
    try:
        table.put_item(Item=user)
        return user
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_device(id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_devices():
    try:
        response = table.scan(
            AttributesToGet=["id", "name"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)