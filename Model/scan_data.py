from pydantic import BaseModel

class ScanData(BaseModel):
    reservation_id : str
    user_id : str
    admin_secret : str