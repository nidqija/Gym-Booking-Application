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

            else :
                booking["session_name"] = "Unknown Session"
                booking["start_time"] = "Unknown Start Time"
                booking["end_time"] = "Unknown End Time"
                
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
    

    @staticmethod
    async def update_booking(booking_id: str, session_id: str, current_user: str):
        updated_booking = await Booking.update_booking(booking_id, current_user, new_status="CHECKED_IN")
        if not updated_booking:
          print(f"Update failed for booking {booking_id}")
          return None

        # Defensive Check 2: Does the session exist?
        session_data = await Session.get_session_by_id(session_id)
        
        if session_data:
            updated_booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
            updated_booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
            updated_booking["end_time"] = session_data.get("end_time", "Unknown End Time")
        else:
            # Provide fallbacks if the session is missing
            print(f"Warning: Session {session_id} not found in database.")
            updated_booking["session_name"] = "Unknown Session"
        
        return updated_booking
    

    @staticmethod
    async def update_booking_by_fullname(full_name: str, new_status: str = "CHECKED_IN"):
        updated_booking = await Booking.update_booking_by_fullname(full_name, new_status)
        if not updated_booking:
          print(f"Update failed for booking with full name {full_name}")
          return None

       
        return updated_booking
    

    @staticmethod
    async def get_booking_by_fullname(full_name: str):
        booking = await Booking.get_booking_by_fullname(full_name)
        if booking:
            session_id = booking.get("session_id")
            if session_id:
                session_data = await Session.get_session_by_id(session_id)
                
                booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
                booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
                booking["end_time"] = session_data.get("end_time", "Unknown End Time")
            else:
                booking["session_name"] = "Unknown Session"
                booking["start_time"] = "Unknown Start Time"
                booking["end_time"] = "Unknown End Time"
        return booking
    

    @staticmethod
    async def get_booking_by_email(email: str):
        """Get the first active (non-checked-in) booking by email"""
        bookings = await Booking.get_bookings_by_user(email)
        
        # Find first booking that's not already checked in
        for booking in bookings:
            if booking.get("status") != "CHECKED_IN":
                session_id = booking.get("session_id")
                if session_id:
                    session_data = await Session.get_session_by_id(session_id)
                    booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
                    booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
                    booking["end_time"] = session_data.get("end_time", "Unknown End Time")
                else:
                    booking["session_name"] = "Unknown Session"
                    booking["start_time"] = "Unknown Start Time"
                    booking["end_time"] = "Unknown End Time"
                return booking
        
        return None

    @staticmethod
    async def update_booking_by_email(email: str, new_status: str = "CHECKED_IN"):
        """Update the first active booking for a given email"""
        booking = await BookingService.get_booking_by_email(email)
        
        if not booking:
            print(f"Update failed: No active booking found for email {email}")
            return None
        
        booking_id = booking.get("booking_id")
        session_id = booking.get("session_id")
        
        updated_booking = await Booking.update_booking(booking_id, email, new_status)
        if not updated_booking:
            print(f"Update failed for booking {booking_id}")
            return None
        
        # Add session details to updated booking
        if session_id:
            session_data = await Session.get_session_by_id(session_id)
            if session_data:
                updated_booking["session_name"] = session_data.get("available_sessions", "Unknown Session")
                updated_booking["start_time"] = session_data.get("start_time", "Unknown Start Time")
                updated_booking["end_time"] = session_data.get("end_time", "Unknown End Time")
        
        return updated_booking
    

    



   
    
    
