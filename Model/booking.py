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
    

    




    


