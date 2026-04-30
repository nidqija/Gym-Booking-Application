
from pydantic import BaseModel, EmailStr 
from Model.database_service import db


class Booking(BaseModel):
    booking_id: str
    user_id: str
    session_id: str
    date: str

    def save(self):
        # this method is for saving the booking data to the database
        booking_data = self.model_dump()

        # change the booking_id field to booking_id for dynamodb schema
        booking_data["booking_id"] = booking_data.pop("booking_id")

        # save the booking data to dynamodb and return the response
        return db.table("Bookings").put_item(Item=booking_data)
    

    def get_booking(self , current_user: str):
        # this method is for retrieving the booking data from the database
        response = db.table("Bookings").get_item(Key={"booking_id": self.booking_id , "user_id": current_user})
        return response.get("Item", None)
    
    # dont need to create an instance of the booking class to call this method, so we use static method
    @staticmethod 
    async def get_bookings_by_user(current_user: str):
        # this method is for retrieving all bookings of a user from the database
        # use query and not scan to retrieve the data based on user_id and booking_id as the partition key and sort key respectively
        # use scan only if we want to retrieve all bookings without filtering by user_id
        response = db.table("Bookings").query(
            IndexName="UserBookingIndex",  
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": current_user}
        )
        return response.get("Items", [])
    

    




    


