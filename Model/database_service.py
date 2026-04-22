import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

DYNAMODB_URL = os.getenv("DYNAMODB_URL", "http://localhost:8000")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "fakeAccessKeyId")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")

# 2. Registry Pattern for Database Management
# used to manage the database connection and table definitions in a centralized way
# avoid scattering database connection logic and table definitions across the codebase
# improve maintainability and scalability by having a single place to manage database interactions
# in a way , it is like a singleton pattern but with more flexibility and separation of concerns

class DatabaseRegistryManager:
    def __init__(self , db_resource):
        self.db_resource = db_resource


    # this method will be used to test connection to the database and return the resource object
    def get_db_resource():
      return boto3.resource(
         "dynamodb",
          endpoint_url=DYNAMODB_URL,
          region_name="us-west-2",
          aws_access_key_id=AWS_ACCESS_KEY_ID,
          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
      )
    
    # this method will be used to create tables in the database based on the definitions
    def get_definitions(self):
       """Define all tables for the gym booking system and return them as a list of dictionaries."""

       return [
          {
             # 1. create table
             "TableName": "Users",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                    
                ],
              # 2. define attributes
                "AttributeDefinitions": [
                   # we only have one attribute which is user_id of type string
                   # if we want integer , we can use "N"    
                    {"AttributeName": "user_id", "AttributeType": "S"}
                ],

                # 3. define provisioned throughput (for local testing we can set it to low values)
                # provisioned throughput is a way to specify how much read and write capacity we want for the table
                # this is required for reading and writing data
                "ProvisionedThroughput": {
                   # set read and write capacity units to 5 
                   # this is required for reading and writing data to the table
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                },    
          },
          {
             "TableName": "Bookings",
                "KeySchema": [
                    {"AttributeName": "booking_id", "KeyType": "HASH"}
                ],

                "AttributeDefinitions": [
                    {"AttributeName": "booking_id", "AttributeType": "S"}
                ],

                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                },
          }
       ]







