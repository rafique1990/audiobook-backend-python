from fastapi import APIRouter, Request, Depends, Form, Cookie
from fastapi.templating import Jinja2Templates

from starlette.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
