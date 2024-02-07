from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import models
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Admin, UpdateAdmin,Department,UpdateDepartment
import utilis,schema,oauth2
from fastapi.security import OAuth2PasswordRequestForm


app = APIRouter(
    prefix="/api/v1"
)


@app.post("/login", response_model=schema.Token)
async def login(admin_user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_model = db.query(models.Admin).filter(
        models.Admin.email == admin.username).first()
    if not admin_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    if not utils.verify(admin.password, admin_model.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid password")

    # create a token
    access_token = oauth2.create_access_token(data={"email": admin_model.email})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/admin-user")
def create_admin(admin: Admin,  db: Session = Depends(get_db)):
    admin_model = db.query(models.Admin).filter(
        models.Admin.username == admin.username ,
        models.Admin.email == admin.email
    ).first()
    if admin_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: {admin.username} or with email:{admin.email} already exists")

    admin_model = models.Admin(**admin.model_dump())

    db.add(admin_model)
    db.commit()

    return admin

@app.put("/update-admin/{admin_username}")
def update_admin(admin_username :str, admin : UpdateAdmin, db: Session = Depends(get_db)):    
    admin_model =  db.query(models.Admin).filter(models.Admin.username == admin_username).first()  
    
    if admin_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {admin_username} does not exists")

    if admin.email != None:       
       admin_model.email =  admin.email

    db.add(admin_model)
    db.commit()
         
    return admin       

@app.get("/admin")
def get_all_admin(token: Annotated[str, Depends(oauth2.oauth2_scheme)], db: Session = Depends(get_db)):
    return db.query(models.Admin).all()

