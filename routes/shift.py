from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Shift,  UpdateShift, Usershift, UpdateUsershift
from datetime import datetime, date, timedelta, timezone


app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-shift")
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

@app.put("/update-shift/")
def update_shift(shift_id :str, shift: UpdateShift, db: Session = Depends(get_db)):    
    shift_model =  db.query(models.User).filter(models.Shift.id == shift_id).first()  
    
    if shift_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {user_name} does not exists")
    
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

@app.get("/shift-created-by-admin")
def get_all_shifts(db: Session = Depends(get_db)):
    return db.query(models.Shift).all()


@app.post("/create-usershift")
def create_usershift(usershift: UpdateUsershift,  db: Session = Depends(get_db)):
    usershift_model = db.query(models.Usershift).filter(
        models.Usershift.user_id  == usershift.user_id).first()
    if usershift_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: User {usershift.user_id} has  already  this shift")

    usershift_model = db.query(models.Usershift).filter(
        models.Usershift.shift_id == usershift.shift_id).first()   
    if usershift_model is   None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: Shift {usershift.shift_id} has not yet been created ")

    usershift_model = models.Usershift(**usershift.model_dump())

    db.add(usershift_model)
    db.commit()

    return usershift


@app.put("/update-user's-shift/")
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

@app.get("/User's-shift")
def get_all_usershifts(db: Session = Depends(get_db)):
    return db.query(models.Usershift).all()