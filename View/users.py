from fastapi import APIRouter, FastAPI, Request
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


