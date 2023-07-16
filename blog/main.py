from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models,hashing
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from routers import blog


app = FastAPI()

models.Base.metadata.create_all(engine)

# app.include_router(authentication.router)
app.include_router(blog.router)
# app.include_router(user.router)




@app.post("/blog", status_code=201,response_model=schemas.ShowBlog,tags=['blogs'])
def create(request: schemas.Blog, db=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# @app.get("/blog",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog],tags=['blogs'])
# def all(db=Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['blogs'])
def show(id: int, response: Response, db=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:       
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} is not available"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )

    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(db=Depends(get_db)):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    db.commit()
    return "done"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id: int, request: schemas.Blog, db=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.update(request)
    db.commit()
    return "updated"



@app.post('/user',tags=['users'])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(name=request.name,email= request.email,password= hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['users'])
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    
    return user