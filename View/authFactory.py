from enum import Enum
from abc import ABC, abstractmethod
from Model.database_service import db



# 1. Factory Pattern
# this is a factory pattern implementation for creating different types of authentication pages.


# we can use this factory to create different types of authentication actions 
# such as sign in and sign up.
class AuthAction(ABC):
    @abstractmethod
    def execute( self , data:dict):
        pass



# Product 1 : Sign In Action
class SignInAction(AuthAction):
    async def execute(self, data: dict):
        # check user credentials and return a response
        response = db.table("Users").get_item(
            Key={
                "user_id": data.get("email")
            }
        )
        
        return f"Logging in user with email: {data.get('email')}, response: {response}"
    

# Product 2 : Sign Up Action
class SignUpAction(AuthAction):
  async def execute(self, data: dict):
        # add user to the database using the provided data
        return db.table("Users").put_item(
            Item={
                "user_id": data.get("email"),
                "full_name": data.get("fullname"),
                "password": data.get("password")
            }
        )
    

# Concrete Factory 
# this factory creates authentication actions based on the action type provided.
class AuthFactory:
    @staticmethod
    # creates an authentication action based on the provided action type (signin or signup)
    # if the action type is not recognized , it raises a value error
    def create_auth_action(action_type: str) -> AuthAction:
        if action_type == "signin":
            return SignInAction()
        elif action_type == "signup":
            return SignUpAction()
        else:
            raise ValueError(f"Unknown auth action type: {action_type}")


