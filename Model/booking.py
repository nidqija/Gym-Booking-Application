
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
    

    @staticmethod
    async def delete_booking(booking_id: str):
        # this method is for deleting a booking from the database based on the booking_id
        response = db.table("Bookings").delete_item(Key={"booking_id": booking_id})
        return response.get("ResponseMetadata", {}).get("HTTPStatusCode", None)
    

    @staticmethod
    async def get_booking_by_session(session_id: str , current_user: str):
        # this method is for retrieving a booking from the database based on the session_id and user_id
        response = db.table("Bookings").query(
            IndexName="SessionBookingIndex",  
            KeyConditionExpression="session_id = :session_id AND user_id = :user_id",
            ExpressionAttributeValues={":session_id": session_id, ":user_id": current_user}
        )
        items = response.get("Items", [])
        return items[0] if items else None
    

    @staticmethod
    async def get_booking_by_id(booking_id: str , current_user: str):
        response = db.table("Bookings").get_item(Key={"booking_id": booking_id})
        booking = response.get("Item")

        # Security Check: Ensure the booking actually belongs to the person requesting it
        if booking and booking.get("user_id") != current_user:
            return None
            
        return booking
    

    




    


