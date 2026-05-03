from Patterns.Decorator.qr_base import QRCodeBase
from Patterns.Service.booking_service import BookingService
from io import BytesIO
import base64
import qrcode

class QRCodeDecorator:
    # method to initialize the decorator with the booking object
    def __init__(self, booking):
        self.booking = booking

    # method to get the booking details and generate a qr code based on the booking information
    def __getitem__(self, key):

        return self.booking[key]

    # method to generate a qr code based on the booking information
    # async method to handle async booking service call

    async def generate_qr_code(self):

        booking_data = await BookingService.get_booking_by_id(self.booking["booking_id"], self.booking["user_id"])

        if booking_data:
            qr_data = (
                f"Booking ID: {booking_data.get('booking_id')}\n"
                f"User ID: {booking_data.get('user_id')}\n"
                f"Session ID: {booking_data.get('session_id')}\n"
                f"Date: {booking_data.get('date')}\n"
            )
            self._qr_data = qr_data
            return QRCodeBase.generate_qr_code(qr_data)
            
        return getattr(self, "_qr_data", None)
    

    async def generate_qr_base64(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"BookingID:{self.booking['booking_id']}")
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_str



    async def print_terminal_qr_code(self):
        """Print the QR as ASCII in terminal using the raw qr data.

        Ensure `generate_qr_code` has been accessed so `_qr_data` exists.
        """
        # ensure raw data exists
        if not hasattr(self, "_qr_data"):
            _ = await self.generate_qr_code()
        QRCodeBase.print_ascii(self._qr_data, invert=True, tty=False)

    
    
        


    
