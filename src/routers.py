import base64
from typing import List, Optional
import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends, UploadFile,File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.db import SessionLocal
from .models import Item, Comment, Catalogue
from typing_extensions import Annotated


templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request, db:Session = Depends(get_db)):
    db_item = db.query(Item).all()
    db_catalogue = db.query(Catalogue).all()
    return templates.TemplateResponse(request=request, name="items.html", context={'items': db_item, 'catalogue': db_catalogue})


@router.get("/videos", response_class=HTMLResponse)
async def read_video(request: Request, db:Session = Depends(get_db)):
    db_item = db.query(Item).all()
    db_catalogue = db.query(Catalogue).all()
    return templates.TemplateResponse(request=request, name="videos.html", context={'items': db_item, 'catalogue': db_catalogue})


@router.get("/detail/{id}", response_class=HTMLResponse)
async def read_detail(id:int, request: Request,db:Session = Depends(get_db)):
    db_detail = db.query(Item).filter(Item.id == id).first()
    results = db_detail.__dict__
    c_id = results['catalogue_id']
    db_related = db.query(Item).filter(Item.catalogue_id == c_id).all()
    db_catalogue = db.query(Catalogue).all()
    return templates.TemplateResponse(request=request, name="detail.html", context={'item':db_detail,'catalogue': db_catalogue, 'relateds':db_related})

@router.get("/catalog/{id}", response_class=HTMLResponse)
async def catalog_type(id:int, request: Request, db:Session = Depends(get_db)):
    db_detail = db.query(Item).filter(Item.catalogue_id == id).all()
    item = db_detail
    return templates.TemplateResponse(request=request, name="items.html", context={'items':item})

@router.get("/search/", response_class=HTMLResponse)
async def search(request: Request, db:Session = Depends(get_db),title: Optional[str] = None):
    db_result = db.query(Item).filter(Item.title == title).all()
    item = db_result
    return templates.TemplateResponse(request=request, name="items.html", context={'items': item})

@router.post("/comments/")
async def comment(request: Request, db:Session = Depends(get_db),name: str = Form(), email: str = Form(), message: str = Form()):
    comment = Comment(name=name, email=email,text=message)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return templates.TemplateResponse(request=request, name="contact.html")


@router.get("/contact", response_class=HTMLResponse)
def read_contact(request: Request, db:Session = Depends(get_db)):
    db_catalogue = db.query(Catalogue).all()
    return templates.TemplateResponse(request=request, name="contact.html", context={'catalogue': db_catalogue})