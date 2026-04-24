from fastapi import APIRouter, FastAPI, Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from View.pageFactory import  PageType,  PageFactory

# user interface router
# use this router to render the home page and other pages
router = APIRouter(tags=["User Interface"])
templates = Jinja2Templates(directory="Template")

# home page 
@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request):  
    page_factory = PageFactory.create_page(PageType.HOME)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)


@router.get("/schedule", response_class=HTMLResponse)
async def render_schedule(request: Request):  
    page_factory = PageFactory.create_page(PageType.BOOKING)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)


@router.get("/sign-in", response_class=HTMLResponse)
async def render_sign_in(request: Request):  
    page_factory = PageFactory.create_page(PageType.SIGN_IN)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)

@router.get("/sign-up", response_class=HTMLResponse)
async def render_sign_up(request: Request):
    page_factory = PageFactory.create_page(PageType.SIGN_UP)
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)
