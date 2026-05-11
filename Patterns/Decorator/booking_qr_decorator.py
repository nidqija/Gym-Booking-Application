from collections import UserDict
from Patterns.Decorator.qr_base import QRCodeBase
from Patterns.Service.booking_service import BookingService


class BookingQRDecorator(UserDict):
    
    # this class is a decorator for the booking service that adds qr code generation functionality
    def __init__(self, booking_data:str):
        self.booking_data = booking_data
        self.qr_code = None

    # this method generates a qr code based on the booking data and returns it as a base64 encoded string
    async def generate_qr_code(self):

        if not self.qr_code:
            qr_content =(
                f"Booking Details:\n"
                f"{self.booking_data}\n"

            )

            self.qr_code = QRCodeBase.generate_qr_code(qr_content)

        return self.qr_code
    
    # this method prints the booking details and the qr code in ascii format to the console for testing purposes
    def print_to_console(self):
        qr_content = f"Booking Details:\n{self.booking_data}\n"

        print(qr_content)
        QRCodeBase.print_ascii(qr_content, invert=True, tty=True)