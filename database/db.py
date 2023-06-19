from boto3 import resource
from os import getenv

dynamodb = resource("dynamodb",
         aws_access_key_id='#',
         aws_secret_access_key='#',
         region_name='#')


tables = [
    {
        "TableName": "users",
        "KeySchema": [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
    },
    {
        "TableName": "station",
        "KeySchema": [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
    },
    {
        "TableName": "device",
        "KeySchema": [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
    },
]

def create_tables():
    try:
        for table in tables:
            dynamodb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
                BillingMode='PAY_PER_REQUEST'
            )
    except Exception as e:
        print(e)
