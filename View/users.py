from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from View.pageFactory import  PageType,  PageFactory 
from View.authFactory import AuthFactory
from Model.database_service import db
from fastapi.responses import RedirectResponse
from fastapi import Cookie
from typing import Optional
from View.dependency import get_current_user


# user interface router
# use this router to render the home page and other pages
router = APIRouter(tags=["User Interface"])
templates = Jinja2Templates(directory="Template")


# home page 
@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request, user_email = Depends(get_current_user)):
    if user_email:
        print(f"User session: {user_email}")

    page_factory = PageFactory.create_page(PageType.HOME)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": user_email} , request=request)


@router.get("/schedule", response_class=HTMLResponse)
async def render_schedule(request: Request, user_email = Depends(get_current_user)):  
    page_factory = PageFactory.create_page(PageType.BOOKING)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": user_email} , request=request)


@router.get("/sign-in", response_class=HTMLResponse)
async def render_sign_in(request: Request, user_email = Depends(get_current_user)):  
    page_factory = PageFactory.create_page(PageType.SIGN_IN)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": user_email} , request=request)


@router.get("/sign-up", response_class=HTMLResponse)
async def render_sign_up(request: Request, user_email = Depends(get_current_user)):  
    page_factory = PageFactory.create_page(PageType.SIGN_UP)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": user_email} , request=request)



@router.post("/auth/{mode}" , response_class=HTMLResponse)
async def render_auth_page(request: Request , mode: str):  
    # this variable will receive the form data from user
    form_data = await request.form()

    # convert the form data to a dictionary for easier access
    data = dict(form_data)

    try:
        # check the mode and respond accordingly
        # calls factory to create the appropriate authentication action 
        # based on the mode (signin or signup)
        action = AuthFactory.create_auth_action(mode)

        # execute the authentication action and get the result
        result = await action.execute(data)

        if mode == "signup":
            # if signup successed
            # return a success message to the user
            if result.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
                return "<div>Sign up successful!</div>"
            else:
                return "<div>Sign up failed. Please try again.</div>"
        
        if mode == "signin":
            # if signin successed
            # return a success message to the user
            if  "Sign in successful" in result:
                response = Response(status_code=204) # 204 = No Content (very fast)
                response.set_cookie(key="user_email", value=data.get("email"), httponly=True) # set a cookie to keep the user logged in
                response.headers["HX-Redirect"] = "/" 
                print("Cookie set for user:", data.get("email")) 
                return response
                
            else:
                return "<div>Sign in failed. Invalid email or password.</div>"

        print(result)

    except ValueError as e:
        # if mode is not recognized
        # print the error and return an error page
        print(f"Error: {e}")
        return "<div>Invalid authentication mode. Please try again.</div>"




"""
@router.post("/auth/signup", response_class=HTMLResponse)
async def handle_sign_up(request: Request):
    form_data = await request.form()
    full_name = form_data.get("full_name")
    email = form_data.get("email")
    password = form_data.get("password")

    dbOperation = db.table("Users").put_item(
         Item={
             "user_id": email,
             "full_name": full_name,
             "password": password
         }
      )
    
    if dbOperation["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return templates.TemplateResponse(name="signup_success.html", context={"request": request} , request=request)
    
    else :
        return templates.TemplateResponse(name="signup_failure.html", context={"request": request} , request=request)
"""