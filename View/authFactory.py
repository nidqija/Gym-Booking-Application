from enum import Enum
from abc import ABC, abstractmethod
from Model.database_service import db
from Model.users import User



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
        # authenticate the user using the provided data

        try :
            user = User.get(email=data.get("email"))
            if user and user.password == data.get("password"):
                response = {"message": "Sign in successful"}
                
            else:
                response = {"message": "Invalid email or password"}

        except Exception as e:
            print(f"DEBUG SIGNIN ERROR: {e}") 
            response = {"error": str(e)}
        
        return f"Logging in user with email: {data.get('email')}, response: {response}"
    

# Product 2 : Sign Up Action
class SignUpAction(AuthAction):
  async def execute(self, data: dict):
        # add user to the database using the provided data
        try:
            new_user = User(
                email=data.get("email"),
                full_name=data.get("fullname"),
                password=data.get("password")
            )

            result =new_user.save()
            return result
        except Exception as e:
            print(f"DEBUG SIGNUP ERROR: {e}") # This will show in your terminal
            return {"error": str(e)}
            
    

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


