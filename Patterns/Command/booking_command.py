from pydantic import BaseModel
from Model.booking import Booking
from abc import ABC, abstractmethod



class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass


class CreateBookingCommand(Command):
    # this command is for creating a new booking and saving it to the database
    def __init__(self, booking_id: str, user_id: str, session_id: str, date: str):
        self.booking_id = booking_id
        self.user_id = user_id
        self.session_id = session_id
        self.date = date

    # overriding the method to create a new booking and saving it to the database
    async def execute(self):
        booking = Booking(
            booking_id=self.booking_id,
            user_id=self.user_id,
            session_id=self.session_id,
            date=self.date
        )
        return booking.save()
    

# we can extend this pattern with other commands like update booking, delete booking, etc. 
# by creating new command classes that inherit from the Command class and implementing the execute method accordingly.