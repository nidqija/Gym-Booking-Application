import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

DYNAMODB_URL = os.getenv("DYNAMODB_URL", "http://localhost:8000")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "fakeAccessKeyId")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")


class DatabaseRegistryManager:
    # this class will manage the database connection and provide methods to create tables and get table references
    def __init__(self , db_resource):
        self.db_resource = db_resource # resource object for dynamodb connection
        self._tables = {} # empty dictionary to store table references for caching purposes


    @staticmethod # static method to create a database resource connection to dynamodb using boto3 library
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
              "TableName" : "Sessions",
                "KeySchema": [
                        {"AttributeName": "session_id", "KeyType": "HASH"}
                    ],
    
                    "AttributeDefinitions": [
                        {"AttributeName": "session_id", "AttributeType": "S"}
                    ],
    
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    },
          } ,
          {
              "TableName" : "GymAvailability",
                "KeySchema": [
                        {"AttributeName": "gym_available_id", "KeyType": "HASH"}
                    ],
    
                    "AttributeDefinitions": [
                        {"AttributeName": "gym_available_id", "AttributeType": "S"}
                    ],
    
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 4,
                        "WriteCapacityUnits": 4
                    },
          },
          {
              # this is how to make a table with a global secondary index (GSI) 
              # to allow querying by user_id in the Bookings table
              "TableName" : "Bookings",
                "KeySchema": [
                        {"AttributeName": "booking_id", "KeyType": "HASH"} ,
                        
                    ],
    
                    "AttributeDefinitions": [
                        {"AttributeName": "booking_id", "AttributeType": "S"},
                        # add user id attribute for global secondary index 
                        {"AttributeName": "user_id", "AttributeType": "S"},
                    ],

                    # define a global secondary index on user_id to allow querying bookings by user_id
                   "GlobalSecondaryIndexes": [
                       {
                           # create a global secondary index on user id to allow querying bookings by user id
                           "IndexName": "UserBookingIndex",
                           "KeySchema": [
                               {"AttributeName": "user_id", "KeyType": "HASH"}
                           ],
                           "Projection": {
                               "ProjectionType": "ALL"
                           },
                            "ProvisionedThroughput": {
                                 "ReadCapacityUnits": 5,
                                 "WriteCapacityUnits": 5
                            },
                       }
                   ],
                       
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    },
                    
          }
       ]
    
    def migrate(self):
        #1. get the list of existing tables in the database
        existing_tables = [table.name for table in self.db_resource.tables.all()]

        #2. perform check and create tables based on the definitions
        for table_def in self.get_definitions():
           table_name = table_def["TableName"]
           # if the table does not exist in the current database, create it
           if table_name not in existing_tables:
              print(f"Creating table: {table_name}")
              self.db_resource.create_table(**table_def)
            # if the table already exists, we can skip it and print a check message
           else:
                print(f"Table {table_name} already up to date. Skipping creation.")


    def table(self, table_name):
        # this method will be used to get a reference to a table in the database
        if table_name not in self._tables:
            self._tables[table_name] = self.db_resource.Table(table_name)
        return self._tables[table_name]
    
# create a db resource connection and init the database registry manager
# then call the migrate method to create tables if they do not exist
resource = DatabaseRegistryManager.get_db_resource()

# initalize the database registry manager with the resource connection
db = DatabaseRegistryManager(resource)

# call the migrate method to migrate the database and create tables if they do not exist
db.migrate()



#benefits of this approach:
#1. we can easily manage the database connection and table references in a single class
#2. we can easily add new tables by simply adding new definitions to the get_definitions method
#3. we can easily migrate the database by calling the migrate method 





