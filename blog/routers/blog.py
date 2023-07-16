from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
# from ..repository import blogs
from repository import blog
router = APIRouter()

get_db= database.get_db

@router.get("/blog",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog],tags=['blogs'])
def all(db=Depends(get_db)):
    
    return blog.get_all(db)
