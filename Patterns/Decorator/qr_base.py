import qrcode
import io
import base64


class QRCodeBase:
    # this function is used 
    def __init__(self, data: str):
        self.data = data

    # this method generates a qr code image based on the provided data
    # returns the qr code image as a base64 encoded string that can be used in an HTML img tag
    # will log into terminal to test the generated qr code string
    @staticmethod
    def generate_qr_code(data: str) -> str:
        #1. instantiate the object with the version , box size and border size
        qr = qrcode.QRCode(version=1, box_size=10, border=5)

        #2. add data to the qr code object
        qr.add_data(data)

        #3. generate the qr code image
        qr.make(fit=True)

        #4. save the qr code image to a bytes buffer and encode it as a base64 string
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # encode the image as a base64 string and return it 
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"

    @staticmethod
    def print_ascii(data: str, invert: bool = False, tty: bool = False) -> None:
        
        # instantiate the QR code object with minimal settings for terminal display
        qr = qrcode.QRCode(version=1, box_size=1, border=2)

        # add data from decorator to the QR code object
        qr.add_data(data)

        # generate the QR code matrix
        qr.make(fit=True)
        # call library helper to print ascii representation
        qr.print_ascii(out=None, tty=tty, invert=invert)