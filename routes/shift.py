from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models,oauth2
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Shift,  UpdateShift, Usershift, UpdateUsershift
from datetime import datetime, date, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from config import settings




app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-shift", tags=["AdminRoutes"]) #by admin
def create_shift(shift: Shift,  db: Session = Depends(get_db)):
    shift_model = db.query(models.Shift).filter(
        models.Shift.role_id  == shift.role_id).first()
    if shift_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: {Shift.role_id} is  already created")

    shift_model = models.Shift(**shift.model_dump())
    

    db.add(shift_model)
    db.commit()
    return shift

@app.put("/update-shift/", tags=["AdminRoutes"]) #by admin
def update_shift(shift_id :str, shift: UpdateShift, db: Session = Depends(get_db)):    
    shift_model =  db.query(models.User).filter(models.Shift.id == shift_id).first()  
    
    if shift_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {shift_id} does not exists")
    
    if shift.no_of_resources != None:
        shift_model.no_of_resources = shift.no_of_resources

    if shift.start_time != None:       
       shift_model.start_time =  shift.start_time

    if shift.end_time != None:
       shift_model.end_time = shift.end_time

    if shift.date_created!= None:
        shift_model.date =shift.date_created

    db.add(shift_model)
    db.commit()
         
    return shift   

@app.get("/shift-created-by-admin", tags=["AdminRoutes"]) #admin
def get_all_shifts(db: Session = Depends(get_db)):
    return db.query(models.Shift).all()


@app.post("/create-usershift", tags=["UserRoutes"]) #user
def create_usershift(token: Annotated[str, Depends(oauth2.user_oauth2_schema)],usershift: UpdateUsershift,  db: Session = Depends(get_db)):
    
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")

    
    # #check if user with id exist
    # usershift_model = db.query(models.Usershift).filter(
    #     models.Usershift.user_id  == user_id).first()
    # if usershift_model is not None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #     detail=f"message: User {user_id} has  already  this shift")

    # check if shift has been created 
    shift_model = db.query(models.Shift).filter(
        models.Shift.id == usershift.shift_id).first()   
    if shift_model is   None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: Shift {usershift.shift_id} has not yet been created ")
    
    #check if the user can apply for the shift based on the role
    userrole_model = db.query(models.UserRole).filter(
        models.UserRole.user_id  == user_id,
        models.UserRole.role_id == shift_model.role_id).first()

    if userrole_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: You cannot apply for shift: {usershift.shift_id} because you didnt register for the role ")


    #check if user has already register for the shift
    usershift_model = db.query(models.Usershift).filter(
        models.Usershift.shift_id == usershift.shift_id,
        models.Usershift.user_id == user_id
        ).first()   
    if usershift_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: user: {user_id} has already registered for shift {usershift.shift_id}")

    #check if the shift has not been fully booked
    # count all users registered for the shift
    shift_registered_user_model = db.query(models.Usershift).filter(models.Usershift.shift_id == usershift.shift_id).all()
   
    # if total registered user is greater than or equal shift no of resources 
    if len(shift_registered_user_model) >= shift_model.no_of_resources:  
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: shift: {shift_model.id} has been fully booked")

    usershift_model = models.Usershift(**usershift.model_dump())
    usershift_model.user_id =user_id

    db.add(usershift_model)
    db.commit()

    return usershift


@app.put("/update-user-shift/", tags=["UserRoutes"])
def update_usershift(user_id :str, usershift: UpdateUsershift, db: Session = Depends(get_db)):    
    usershift_model =  db.query(models.UserShift).filter(models.User.id == user_id).first()  
    
    if usershift_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {user_id} does not exists")
    
    if usershift.shift_id != None:
        usershift_model.shift_id = usershift.shift_id

    if usershift.date_created != None:
       usershift_model.date_created = usershift.date_created

    db.add(usershift_model)
    db.commit()
         
    return usershift   

@app.get("/Users-shift", tags=["AdminRoutes"])
def get_all_usershifts(db: Session = Depends(get_db)):
    return db.query(models.Usershift).all()


@app.get("/get-usershift/{user_id}", tags=["UserRoutes"])
def get_usershift(user_id: int = Path (description= "The ID of Users", gt=0, le=100000),db: Session = Depends(get_db)):
    user_shift_model =  db.query(models.Usershift).filter(models.Usershift.user_id == user_id).all() 
    
    if user_shift_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: User id  {user_id} does not  exists")
    
    return user_shift_model 

@app.get("/get-shift/{shift_id}", tags=["AdminRoutes"])
def get_shift(shift_id: int = Path (description= "The ID of shift", gt=0, le=100000),db: Session = Depends(get_db)):
    user_shift_model =  db.query(models.Usershift).filter(models.Usershift.shift_id == shift_id).all() 
    
    if user_shift_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: Shift id  {shift_id} does not  exists")
    
    return user_shift_model 