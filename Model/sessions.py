from pydantic import BaseModel, EmailStr 
from Model.database_service import db


class Session(BaseModel):
    session_id: str
    available_sessions: str
    start_time: str
    end_time: str
    
    

    def save(self):
        # this method is for saving the session data to the database
        session_data = self.model_dump()

        # change the session_id field to session_id for dynamodb schema
        session_data["session_id"] = session_data.pop("session_id")

        # save the session data to dynamodb and return the response
        return db.table("Sessions").put_item(Item=session_data)
    

    # this method is for getting session information
    # class method is used to get a session based on the session_id and return it as an instance of the Session class
    # other uses of this method can be to get session information for a specific session_id and return it as a dictionary
    @classmethod
    def get_all_sessions(cls):
        # retrieves all available sessions from the database and returns them as a list of Session instances
        response = db.table("Sessions").scan()
        
        # init an empty list to store the session instances
        sessions = []

        # for loop and append the session list with the session instances created from the database items
        for item in response.get("Items", []):
            sessions.append(cls(
                session_id=item["session_id"],
                available_sessions=item["available_sessions"],
                start_time=item["start_time"],
                end_time=item["end_time"]
            ))
        return sessions
    

    @classmethod
    def post(cls, session_id: str, available_sessions: str, start_time: str, end_time: str):
        # this method is for creating a new session and saving it to the database
        session = cls(
            session_id=session_id,
            available_sessions=available_sessions,
            start_time=start_time,
            end_time=end_time
        )
        return session.save()
        
        