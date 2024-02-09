from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models, oauth2
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import UserRole
from typing import Annotated
from config import settings
from jose import JWTError, jwt




app = APIRouter(
    prefix="/api/v1"
)

@app.post("/create-Userroles", tags=["UserRoutes"])
def create_userrole(token: Annotated[str, Depends(oauth2.user_oauth2_schema)],userrole: UserRole,  db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")

    # user_model = db.query(models.User).filter(
    #     models.User.id == user_id 
    # ).first()
    # if user_model is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #     detail=f"mesage: user with id {user_id}, doesnot exist")

    role_model =  db.query(models.Roles).filter(models.Roles.id == userrole.role_id).first()  
    
    if role_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role: {userrole.role_id} does not exists")

    userrole_model = db.query(models.UserRole).filter(
        models.UserRole.user_id  == user_id,
        models.UserRole.role_id == userrole.role_id).first()

    if userrole_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"mesage: Role {userrole.role_id} is  already created for User {userrole.user_id}")

    userrole_model = models.UserRole(**userrole.model_dump())
    userrole_model.user_id = user_id
    db.add(userrole_model)
    db.commit()

    return userrole

@app.get("/userroles", tags=["AdminRoutes"])
def get_all_usersroles(db: Session = Depends(get_db)):
    return db.query(models.UserRole).all()

@app.get("/get-userrole/{user_id}", tags=["UserRoutes"])
def get_userrole(user_id: int = Path (description= "The ID of Users", gt=0, le=100000),db: Session = Depends(get_db)):
    userrole_model =  db.query(models.UserRole).filter(models.UserRole.user_id == user_id).all() 
    
    if userrole_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: User id  {user_id} does not  exists")
    
    return userrole_model    
