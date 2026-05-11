from typing import Optional
from pydantic import BaseModel

class ScanData(BaseModel):
    reservation_id: Optional[str] = None
    user_id: Optional[str] = None
    admin_secret: Optional[str] = None
    session_id: Optional[str] = None