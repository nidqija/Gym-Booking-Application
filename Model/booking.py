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
    

    def book_slot(self):
        # this method is for booking a slot for a user
        # it saves the booking data to the database and updates the available sessions in the Sessions table
        booking_response = self.save()

        # update the available sessions in the Sessions table
        session_response = db.table("Sessions").get_item(Key={"session_id": self.session_id})
        session_item = session_response.get("Item")
        if session_item:
            available_sessions = int(session_item["available_sessions"])
            if available_sessions > 0:
                available_sessions -= 1
                db.table("Sessions").update_item(
                    Key={"session_id": self.session_id},
                    UpdateExpression="SET available_sessions = :val",
                    ExpressionAttributeValues={":val": str(available_sessions)}
                )
                return booking_response
            else:
                return {"error": "No available sessions"}
        else:
            return {"error": "Session not found"}



    


