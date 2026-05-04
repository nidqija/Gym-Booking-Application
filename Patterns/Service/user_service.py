from fastapi import Cookie, Depends
from typing import Optional
from Model.users import User 

def get_user_repository():
    # this is a simple repository function that returns the User class for database operations related to users
    return User

async def get_current_user(
    user_email: Optional[str] = Cookie(default=None),
    user_repo = Depends(get_user_repository),
    user_role: Optional[str] = None
):
    if not user_email:
        return None
    
    
    
    # Now we call the injected repo instead of the Model class directly
    user_obj = user_repo.get(email=user_email)
    user_role_obj = user_obj.getUserInfo() if user_obj else None
    if user_role_obj:
        user_role = user_role_obj.get("role", "user") 
        print(f"DEBUG: User role for {user_email} is {user_role}")
    else:
        print(f"DEBUG: No user found with email {user_email}")

    return user_obj