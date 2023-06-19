from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key, Attr
from fastapi import FastAPI, HTTPException
import hashlib

table = dynamodb.Table("users")
table_device = dynamodb.Table("device")

def create_user(user: dict):
    try:
        email = user.get('email')
        
        # Check if the email already exists in the database
        response = table.scan(
            FilterExpression=Attr("email").eq(email),
            ProjectionExpression="email"
        )
        items = response["Items"]
        if items:
            return JSONResponse(content={"error": "Email already exists"}, status_code=400)
        
        password = user.get('password')
        if password:
            # Hash the password using a secure hashing algorithm (e.g., SHA-256)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user['password'] = hashed_password
        
        table.put_item(Item=user)
        return user
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_user(id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_users():
    try:
        response = table.scan(
            Limit=5,
            AttributesToGet=["email", "id"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def login(login_request: dict):
    try:
        email = login_request["email"]
        password = login_request["password"]

        response = table.scan(
            FilterExpression=Key("email").eq(email),
            ProjectionExpression="#id, #username, #station, #password",
            ExpressionAttributeNames={"#id": "id", "#username": "name", "#station": "station", "#password": "password"}
        )
        items = response["Items"]
        if not items:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        stored_password = items[0]["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if stored_password != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "id": items[0]["id"],
            "name": items[0]["name"],
            "station": items[0]["station"],
            "message": "Login successful"
        }
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_station(id: str, station: list):
    try:
        # Check if the id exists in the station table
        response = table_device.get_item(Key={"id": station[0]})
        if "Item" not in response:
            # Return a specific code or response indicating that the id doesn't exist
            return JSONResponse(content="Id not found in station table", status_code=404)
        
        # Update the station record
        response = table.update_item(
            Key={"id": id},
            UpdateExpression="SET #s = :station",
            ExpressionAttributeNames={"#s": "station"},
            ExpressionAttributeValues={":station": station}
        )
        
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_station(id: str):
    try:
        response = table.update_item(
            Key={"id": id},
            UpdateExpression="SET #s = :empty_list",
            ExpressionAttributeNames={"#s": "station"},
            ExpressionAttributeValues={":empty_list": []}
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def update_user(id: str, name: str = None, surname: str = None, password: str = None, birthday: str = None):
    try:
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        
        if name:
            update_expression += "#n = :name, "
            expression_attribute_names["#n"] = "name"
            expression_attribute_values[":name"] = name
        
        if surname:
            update_expression += "#s = :surname, "
            expression_attribute_names["#s"] = "surname"
            expression_attribute_values[":surname"] = surname
        
        if password:
            # Hash the password using a secure hashing algorithm (e.g., SHA-256)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            update_expression += "#p = :password, "
            expression_attribute_names["#p"] = "password"
            expression_attribute_values[":password"] = hashed_password
        
        if birthday:
            update_expression += "#b = :birthday, "
            expression_attribute_names["#b"] = "birthday"
            expression_attribute_values[":birthday"] = birthday
        
        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")
        
        response = table.update_item(
            Key={"id": id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
