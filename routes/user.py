from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import User, UpdateUser

app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-user")
def create_user(user: User,  db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(
        models.User.name == user.name ,
        models.User.email == user.email
    ).first()

    if user_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: {user.name} or with email:{user.email} or already exists")

    user_model = models.User(**user.model_dump())

    db.add(user_model)
    db.commit()

    return user

@app.put("/update-user/")
def update_user(user_id :str, user: UpdateUser, db: Session = Depends(get_db)):    
    user_model =  db.query(models.User).filter(models.User.id == user_id).first()  
    
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {user_name} does not exists")
    
    if user_model != None:
        user_model.name = user.name

    if user.email != None:       
       user_model.email =  user.email

    if user.phone_number != None:
       user_model.phone_number = user.phone_number

    db.add(user_model)
    db.commit()
         
    return user      

@app.get("/user")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


