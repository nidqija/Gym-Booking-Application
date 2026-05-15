
from pydantic import BaseModel
from Model.database_service import db
from datetime import datetime
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
            # get the item from the response and print it for debugging
            item = response.get("Item")
            print(f"Simple fetch response: {response}")

            # return the item as instance if exists , else return None
            return cls(**item) if item else None
        except Exception as e:
            print(f"Simple fetch failed: {e}")
            return None

    def save(self):
        # This will save/overwrite based ONLY on the gym_available_id
        return db.table("GymAvailability").put_item(Item=self.model_dump())
    

    @staticmethod
    async def create_blocked_dates(dates: list[str], updated_by: str):

        existing_records = GymAvailable.get()

        if existing_records:
            existing_records.blocked_dates = dates
            existing_records.last_updated_by = updated_by
            existing_records.updated_at = datetime.now().isoformat()
            return existing_records.save()
        
        else:
            new_record = GymAvailable(
                blocked_dates=dates,
                last_updated_by=updated_by,
                updated_at=datetime.now().isoformat()
            )
            return new_record.save()
        
        
        