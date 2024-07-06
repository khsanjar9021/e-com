from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, HTTPException, Request
from sqladmin import Admin, ModelView
from .routers import router
from .models import Base
from .db import SessionLocal, engine
from .admin import ItemAdmin, CommentAdmin, CatalogueAdmin, authentication_backend




Base.metadata.create_all(bind=engine)

app = FastAPI()

admin = Admin(app=app, engine=engine,authentication_backend=authentication_backend)



app.mount("/static", StaticFiles(directory="static"), name="static")

admin.add_view(ItemAdmin)
admin.add_view(CommentAdmin)
admin.add_view(CatalogueAdmin)

app.include_router(router=router)










