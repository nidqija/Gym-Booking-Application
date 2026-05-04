from fastapi import APIRouter, Depends,  Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Patterns.Factory.pageFactory import  PageType,  PageFactory 
from Patterns.Factory.authFactory import AuthFactory
from Patterns.Service.user_service import get_current_user
from Patterns.Service.home_service import HomeService
from Patterns.Service.gym_dates_service import GymDatesService
from Patterns.Command.booking_command import CreateBookingCommand
from Patterns.Service.booking_service import BookingService
from Patterns.Decorator.qr_code_decorator import QRCodeDecorator
from datetime import datetime, timedelta
from uuid import uuid4


# user interface router
# use this router to render the home page and other pages
router = APIRouter(tags=["User Interface"])
templates = Jinja2Templates(directory="Template")


# home page 
@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request, current_user= Depends(get_current_user)):
    view_data = HomeService.get_home_data(current_user)  
    page_factory = PageFactory.create_page(PageType.HOME)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, **view_data }, request=request)


@router.get("/schedule", response_class=HTMLResponse)
async def render_schedule(request: Request, current_user = Depends(get_current_user)):  
    blocked = GymDatesService.get_blocked_dates()

    # generate a list of upcoming dates for the next 30 days and mark them as blocked or available
    # init the list
    upcoming = []

    # loop through the next 30 days and add them to the list with the blocked status
    for i in range(31):
        # calculate the date and format it as a string
        date = datetime.now() + timedelta(days=i)
        # format the date as a string in the format of "YYYY-MM-DD" for easier comparison with blocked dates
        date_str = date.strftime("%Y-%m-%d")
        # append the date and its blocked status to the upcoming list
        upcoming.append({
            "date": date_str,
            "is_blocked": date_str in blocked
        })
    view_data = HomeService.get_home_data(current_user)
    page_factory = PageFactory.create_page(PageType.BOOKING)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": current_user, "upcoming": upcoming, **view_data} , request=request)


@router.get("/sign-in", response_class=HTMLResponse)
async def render_sign_in(request: Request, current_user = Depends(get_current_user)):  
    page_factory = PageFactory.create_page(PageType.SIGN_IN)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": current_user} , request=request)


@router.get("/sign-up", response_class=HTMLResponse)
async def render_sign_up(request: Request, current_user = Depends(get_current_user)):  
    page_factory = PageFactory.create_page(PageType.SIGN_UP)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": current_user} , request=request)

@router.get("/my-reservation", response_class=HTMLResponse)
async def render_my_reservation(request: Request, current_user = Depends(get_current_user)):

    user_reservations = []

    page_factory = PageFactory.create_page(PageType.MY_RESERVATION)
    view_data = HomeService.get_home_data(current_user)

    if current_user:
       user_reservations = await BookingService.get_booking_by_user(current_user.email)

    if not current_user:
        user_reservations = []

    template_path = page_factory.get_template_path()    
    return templates.TemplateResponse(name=template_path, context={"request": request, "user": current_user, "reservations": user_reservations, **view_data} , request=request)



@router.post("/reserveslot/{session_id}" , response_class=HTMLResponse)
async def reserve_slot(request: Request, session_id: str, current_user = Depends(get_current_user)):  
    
    if not current_user:
        return "<div>Please sign in to reserve a slot.</div>"
    
    form_data = await request.form()
    booking_date = form_data.get("date")

    command = CreateBookingCommand(
        booking_id=str(uuid4()),  # Generate a unique booking ID
        user_id=current_user.email,  # Get the user ID from the current user
        session_id=session_id,  # Get the session ID from the path parameter
        date=booking_date  # Get the booking date from the form data
    )

    result = await command.execute()  # Execute the command to create the booking

    if result.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        return "<div>Slot reserved successfully!</div>"
    else:
        return "<div>Failed to reserve slot. Please try again.</div>"


@router.post("/cancelreservation/{booking_id}" , response_class=HTMLResponse)
async def cancel_reservation(request: Request, booking_id: str, current_user = Depends(get_current_user)):
    if not current_user:
        return "<div>Please sign in to cancel a reservation.</div>"
    
    command = CreateBookingCommand(
        booking_id=booking_id,  # Get the booking ID from the path parameter
        user_id=current_user.email,  
        session_id="", 
        date=""  
    )

    result = await command.cancel_booking()  

    if result == 200:
        return "<div  class='text-white'>Reservation canceled successfully!</div>"
    else:
        return "<div class='text-white'>Failed to cancel reservation. Please try again.</div>"


# to be implemented

@router.post("/generate_qr/{booking_id}", response_class=HTMLResponse)
async def generate_qr(request: Request, booking_id: str, current_user = Depends(get_current_user)):
    
    form_data = await request.form()

    booking = await BookingService.get_booking_by_id(booking_id, current_user.email)
    if not booking:
        return "<div class='text-white'>Booking not found. Please check your reservation and try again.</div>"
    qr_decorator = QRCodeDecorator(booking)
    qr_code = await qr_decorator.generate_qr_base64()

    return f"""
    <div class='text-white'>
       <div class="mb-4">
        <h2>QR Code for Booking ID: {current_user.email}</h2>
        </div>
        <img src="data:image/png;base64,{qr_code}" 
         alt="Access Pass" 
         class="img-fluid" />
    </div>
    """


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
                return "<div class='text-white'>Sign up successful!</div>"
            else:
                return "<div class='text-white'>Sign up failed. Please try again.</div>"
        
        if mode == "signin":
            # if signin successed
            # return a success message to the user
            if  "Sign in successful" in result:
                user_role = "admin" if "(Admin)" in result else "user"
                print(f"DEBUG: User role determined as {user_role} from result: {result}")
                response = Response(status_code=204) # 204 = No Content (very fast)
                response.set_cookie(key="user_email", value=data.get("email"), httponly=True) # set a cookie to keep the user logged in

                if user_role == "admin":
                    response.headers["HX-Redirect"] = "/admin-dashboard" 
                else:
                    response.headers["HX-Redirect"] = "/"
                print("Cookie set for user:", data.get("email")) 
                
                return response
            
                
            else:
                return "<div>Sign in failed. Invalid email or password.</div>"
            

        if mode == "signout":
             return result

        print(result)

    except ValueError as e:
        # if mode is not recognized
        # print the error and return an error page
        print(f"Error: {e}")
        return "<div>Invalid authentication mode. Please try again.</div>"
    

@router.get("/admin-dashboard", response_class=HTMLResponse)
async def render_admin_dashboard(request: Request, current_user = Depends(get_current_user)):
    # 1. Strict Authorization Check
    is_admin = current_user and current_user.getUserInfo().get("role") == "admin"
    
    if not is_admin:
        # If not admin, redirect to home page immediately
        # Use 303 (See Other) for redirects
        response = Response(status_code=303)
        response.headers["HX-Redirect"] = "/" 
        return response

    # 2. Admin Logic (only runs if authorized)
    try:
        # Use the Factory to get the correct admin page
        page_factory = PageFactory.create_page(PageType.ADMIN_DASHBOARD)
        
        # Gather data for the dashboard
        view_data = HomeService.get_home_data(current_user)
        template_path = page_factory.get_template_path()
        
        return templates.TemplateResponse(name=template_path, context={"request": request, "user": current_user, **view_data} , request=request)

    except Exception as e:
        print(f"Error rendering admin dashboard: {e}")
        return "<div>Error loading dashboard. Please contact system admin.</div>"



