from pydantic import BaseModel
from Model.database_service import db

class GymAvailable(BaseModel):
    # This is your new "gym_available_id"
    # We use a default value so we always hit the same record
    gym_available_id: str = "MAIN_SCHEDULE" 
    blocked_dates: list[str] = []
    gym_status: str = "OPEN"
    last_updated_by: str 
    updated_at: str

    @classmethod
    def get(cls):
        try:
            # SIMPLE LOOKUP: Only one key required
            response = db.table("GymAvailability").get_item(
                Key={"gym_available_id": "MAIN_SCHEDULE"}
            )
            item = response.get("Item")
            print(f"Simple fetch response: {response}")
            return cls(**item) if item else None
        except Exception as e:
            print(f"Simple fetch failed: {e}")
            return None

    def save(self):
        # This will save/overwrite based ONLY on the gym_available_id
        return db.table("GymAvailability").put_item(Item=self.model_dump())