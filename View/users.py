from fastapi import APIRouter, FastAPI, Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from View.pageFactory import DashboardPage, HomePage, SchedulePage

# user interface router
# use this router to render the home page and other pages
router = APIRouter(tags=["User Interface"])
templates = Jinja2Templates(directory="Template")

# home page 
@router.get("/", response_class=HTMLResponse)
async def render_home(request: Request):  
    page_factory = HomePage()
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)


@router.get("/schedule", response_class=HTMLResponse)
async def render_schedule(request: Request):  
    page_factory = SchedulePage()
    template_path = page_factory.get_template_path()
    return templates.TemplateResponse(name=template_path, context={"request": request} , request=request)