from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models,oauth2
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Shift,  UpdateShift, Usershift, UpdateUsershift
from datetime import datetime, date, timedelta, timezone, time
from typing import Annotated
from jose import JWTError, jwt
from config import settings




app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-shift", tags=["AdminRoutes"]) #by admin
def create_shift(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)],shift: Shift,  db: Session = Depends(get_db)):
    shift_model = db.query(models.Shift).filter(
        models.Shift.role_id  == shift.role_id, models.Shift.date_created==shift.date_created ).first()
    if shift_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"message: shift is  already created for  role {shift.role_id}  on {shift.date_created}")

    shift_model = models.Shift(**shift.model_dump())
    

    db.add(shift_model)
    db.commit()
    return shift

@app.put("/update-shift/", tags=["AdminRoutes"]) #by admin
def update_shift(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], shift_id :str, shift: UpdateShift, db: Session = Depends(get_db)):    
    shift_model =  db.query(models.Shift).filter(models.Shift.id == shift_id).first()  
    
    if shift_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {shift_id} does not exists")
    
    if shift.no_of_resources != None:
        shift_model.no_of_resources = shift.no_of_resources

    if shift.role_id != None:
        shift_model.role_id = shift.role_id

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
def create_usershift(token: Annotated[str, Depends(oauth2.user_oauth2_schema)],usershift: UpdateUsershift, 
 db: Session = Depends(get_db)):
    
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")

    
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

    
    # user_shift_details = db.query(models.Usershift, models.Shift).filter(
    #     models.Usershift.shift_id==models.Shift.id, models.Usershift.user_id==user_id ).all()

    # for u,s in user_shift_details: 
    #     if s.date_created == shift_model.date_created:
    #         if (shift_model.start_time >= s.start_time and shift_model.start_time <= s.end_time)or
    #         (shift_model.end_time  >= s.start_time and shift_model.end_time<= s.end_time):
    #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"you cannot be on this shift,because one of your shifts time crossed this new one ")

    usershift_model = models.Usershift(**usershift.model_dump())
    usershift_model.user_id =user_id

    db.add(usershift_model)
    db.commit()

    return usershift


@app.put("/update-user-shift/", tags=["UserRoutes"])
def update_usershift(token: Annotated[str, Depends(oauth2.user_oauth2_schema)], usershift: UpdateUsershift, db: Session = Depends(get_db)): 

    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")   
    usershift_model =  db.query(models.UserShift).filter(models.User.id == user_id).first()  
    
    if usershift_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {user_id} does not exists")
    
    if usershift.shift_id != None:
        usershift_model.shift_id = usershift.shift_id


    db.add(usershift_model)
    db.commit()
         
    return usershift   

@app.get("/Users-shift", tags=["AdminRoutes"])
def get_all_usershifts(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], db: Session = Depends(get_db)):
    return db.query(models.Usershift).all()


@app.get("/get-usershift", tags=["UserRoutes"])
def get_usershift(token: Annotated[str, Depends(oauth2.user_oauth2_schema)],db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")
    user_shift_model =  db.query(models.Usershift).filter(models.Usershift.user_id == user_id).all() 
    
    if user_shift_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: User id  {user_id} does not  exists")
    
    return user_shift_model 

@app.get("/get-shift/{shift_id}", tags=["AdminRoutes"])
def get_shift(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], shift_id: int = Path (description= "Shift ID", gt=0, le=100000),db: Session = Depends(get_db)):
    user_shift_model =  db.query(models.Usershift).filter(models.Usershift.shift_id == shift_id).all() 
    
    if user_shift_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: Shift id  {shift_id} does not  exists")
    
    return user_shift_model 


@app.get("/clock-in/{shift_id}", tags=["UserRoutes"],)
def get_clock_in(token: Annotated[str, Depends(oauth2.user_oauth2_schema)], shift_id: int = Path (description= "Shift ID", gt=0, le=100000),db: Session = Depends(get_db)):
    
    try:
        #decode the token
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]) 
        email: str = payload.get("email")
        user_id: str = payload.get("id")
    except Exception as e: #catch any error while decoding
        if e=="Signature has expired.":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"login expire please login again")

    clock_model =  db.query(models.Usershift).filter(models.Usershift.shift_id == shift_id,
    models.Usershift.user_id == user_id).first() 

    if clock_model  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: User id  {user_id} does not  exists")
    
    #set clock in
    #get the shift by id
    shift_model: models.Shift =  db.query(models.Shift).filter(models.Shift.id == shift_id).first() 
    print(shift_model.date_created)
    #compute time and date
    start_time_str = str(shift_model.date_created) +" "+ str(time(hour=shift_model.start_time, minute=0,second=0))
    start_time_obj = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time_str = str(shift_model.date_created) +" "+ str(time(hour=shift_model.end_time, minute=0,second=0))
    end_time_obj = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
   
    if not (datetime.now() >= start_time_obj and datetime.now() <= end_time_obj):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You cannot clock in, its either the time has passed or its not yet time")

    
    

    clock_model.clock_in = datetime.now() #timne now
    
    db.add(clock_model)
    db.commit()
    return "clocked in" 

@app.get("/clock-out/{shift_id}", tags=["UserRoutes"],)
def get_clock_out(token: Annotated[str, Depends(oauth2.user_oauth2_schema)], shift_id: int = Path (description= "Shift ID", gt=0, le=100000),db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")
    clock_model =  db.query(models.Usershift).filter(models.Usershift.shift_id == shift_id,
    models.Usershift.user_id == user_id).first() 
    
    if clock_model  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message: User id  {user_id} does not  exists")
    
    #set clock out
    shift_model: models.Shift =  db.query(models.Shift).filter(models.Shift.id == shift_id).first() 
    start_time_str = str(shift_model.date_created) +" "+ str(time(hour=shift_model.start_time, minute=0,second=0))
    start_time_obj = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time_str = str(shift_model.date_created) +" "+ str(time(hour=shift_model.end_time, minute=0,second=0))
    end_time_obj = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")


    if datetime.now() >= end_time_obj :
        clock_model.clock_out = datetime.now() #timne now
        db.add(clock_model)
        db.commit()
        print("time has definately pass")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You cannot clock out, because shift has not expired")

    

    return "clocked out"     
