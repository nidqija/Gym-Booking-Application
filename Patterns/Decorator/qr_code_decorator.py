from Patterns.Decorator.qr_base import QRCodeBase


class QRCodeDecorator:
    # method to initialize the decorator with the booking object
    def __init__(self, booking):
        self.booking = booking

    # method to get the booking details and generate a qr code based on the booking information
    def __getitem__(self, key):

        return self.booking[key]

    # method to generate a qr code based on the booking information
    # property decorator is used to make this method a property of the QRCodeDecorator class 
    # so that it can be accessed like an attribute

    @property
    def generate_qr_code(self):
        if self.booking:
            # generate a qr code based on the booking information (raw data)
            qr_data = (
                f"Booking ID: {self.booking.get('booking_id')}\n"
                f"User ID: {self.booking.get('user_id')}\n"
                f"Session ID: {self.booking.get('session_id')}\n"
                f"Date: {self.booking.get('date')}"
            )
            # keep raw data for terminal printing
            self._qr_data = qr_data
            return QRCodeBase.generate_qr_code(qr_data)

    def print_terminal_qr_code(self):
        """Print the QR as ASCII in terminal using the raw qr data.

        Ensure `generate_qr_code` has been accessed so `_qr_data` exists.
        """
        # ensure raw data exists
        if not hasattr(self, "_qr_data"):
            _ = self.generate_qr_code
        QRCodeBase.print_ascii(self._qr_data, invert=True, tty=False)
