from pydantic import BaseModel, EmailStr 
from Model.database_service import db


class User(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    def save(self):
        # this method is for sign up action
        # it saves the user data to the database
        user_data = self.model_dump()

        # change the email field to user_id for dynamodb schema
        user_data["user_id"] = user_data.pop("email")

        # save the user data to dynamodb and return the response
        return db.table("Users").put_item(Item=user_data)
    

    @classmethod
    # this is for sign in action
    def get(cls , email: str):
        response = db.table("Users").get_item(Key={"user_id": email})
        item = response.get("Item")
        if item:
            return cls(
                email=item["user_id"],
                full_name=item["full_name"],
                password=item["password"]
            )
        
        

        return None
    
    def getUserInfo(self):
        # this method is for getting user information
        # it retrieves the user data from the database based on the email and returns it as a dictionary
        response = db.table("Users").get_item(Key={"user_id": self.email})
        item = response.get("Item")
        if item:
            return {
                "email": item["user_id"],
                "full_name": item["full_name"],
                "password": item["password"],
                "role": item.get("role", "user") 
            }
        return None
       
    
