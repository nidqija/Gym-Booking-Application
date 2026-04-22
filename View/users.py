from fastapi import APIRouter, FastAPI, Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from View.pageFactory import PageFactory, PageType

# user interface router
# use this router to render the home page and other pages
router = APIRouter(tags=["User Interface"])
templates = Jinja2Templates(directory="Template")

# home page 
@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request):  
    template_name = PageFactory.get_page(PageType.HOME)
    return templates.TemplateResponse(name=template_name, request=request )


@router.get("/about", response_class=HTMLResponse)
async def render_about(request: Request):
    template_name = PageFactory.get_page(PageType.ABOUT)
    return templates.TemplateResponse(name=template_name, request=request)


@router.get("/schedule" , response_class=HTMLResponse)
async def render_schedule(request: Request):
    template_name = PageFactory.get_page(PageType.SCHEDULE)
    return templates.TemplateResponse(name=template_name, request=request)   

