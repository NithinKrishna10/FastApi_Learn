from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models,hashing
# from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import blog,user,authentication
from . import database

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)