from fastapi import Cookie , Request
from typing import Optional

# helper function to get the current user from the cookie
# called as a dependency in the route handlers to access the user session information
async def get_current_user(request: Request, user_email: Optional[str] = Cookie(default=None)):
    if user_email:
        print(f"User session: {user_email}")
        return user_email
    return None


