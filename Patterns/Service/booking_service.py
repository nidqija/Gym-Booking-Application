from datetime import datetime
from Model.booking import Booking
from Model.sessions import Session


class BookingService:
    
    # this function does not need object state and can be called without creating an instance of the class, 
    # so we use static method
    @staticmethod
    async def get_booking_by_user(current_user: str):
        all_bookings = await Booking.get_bookings_by_user(current_user)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        for booking in all_bookings:
            session_id = booking.get("session_id")

            if session_id:
                session_data = await Session.get_session_by_id(session_id)

                booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
                booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
                booking["end_time"] = session_data.get("end_time", "Unknown End Time")
                
        return all_bookings
    

    # use this method to get a specific booking by session id , it will return the booking details
    # alongside session details
    @staticmethod
    async def get_booking_by_session(session_id: str , current_user: str):
        booking = await Booking.get_booking_by_session(session_id, current_user)

        if booking:
            session_data = await Session.get_session_by_id(session_id)

            booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
            booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
            booking["end_time"] = session_data.get("end_time", "Unknown End Time")
        
        return booking
    

    @staticmethod
    async def get_booking_by_id(booking_id: str , current_user: str):
        booking = await Booking.get_booking_by_id(booking_id, current_user)
        if booking:
            session_id = booking.get("session_id")
            if session_id:
                session_data = await Session.get_session_by_id(session_id)

                booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
                booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
                booking["end_time"] = session_data.get("end_time", "Unknown End Time")
                booking["user_id"] = current_user
        return booking
    

        
    
    
