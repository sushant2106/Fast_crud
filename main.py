from fastapi import FastAPI,Depends,status,Response,HTTPException
from schemas import Blog
import models,schemas
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    
    finally:
        db.close()


models.Base.metadata.create_all(engine)

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all_blog(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK)
def show(id:int,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with the id {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not found")

    return blog



@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def  delete_blog(id:int,db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'Delete':'Deletion Done'}



@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
     #db.query(models.Blog).filter(models.Blog.id==id).update(request)
    x=db.query(models.Blog).filter(models.Blog.id==id).first()
    x.title=request.title
    x.body=request.body
    db.add(x)
   
     
    db.commit()
    return 'updated Sucessfully'




