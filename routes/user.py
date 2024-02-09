from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import models, mail
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import User, UpdateUser
import utils,schema,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from config import settings
from typing import Annotated
from jose import JWTError, jwt





app = APIRouter(
    prefix="/api/v1"
)


@app.post("/user-login", response_model=schema.Token, tags=["AuthRoutes"])
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    if not utils.verify(user_credentials.password, user_model.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid password")

    # create a token
    access_token = oauth2.create_access_token(data={"email": user_model.email, "id": user_model.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create-user-account", tags=["UserRoutes"])
def create_user(background_tasks: BackgroundTasks , user: User,  db: Session = Depends(get_db)):
    
    user_model = db.query(models.User).filter(
        models.User.phone_number == user.phone_number ,
        models.User.email == user.email
    ).first()

    if user_model is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"message: {user.phone_number} or  email:{user.email} or already exists")
   
    #hash the user password before saving to db
    user.password = utils.hash(user.password) 
    #generate email verification code for user
    user_model = models.User(**user.model_dump())
    user_model.email_verification_code = utils.generate_random_string(15)


    db.add(user_model)
    message  = f"Please click the link below to verify your email\n{settings.remote_url}/api/v1/verify/{user_model.email_verification_code}"
    background_tasks.add_task(mail.send_email, user.email, "Welcome on board", message)
    db.commit()
    # try:
    #     # send mail to user
      

    # except Exception as e:
    #      db.rollback()
    #      print(e)
    #      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"message: there was an error creating user")
    



    return user

@app.put("/update-user/", tags=["UserRoutes"])
def update_user(token: Annotated[str, Depends(oauth2.user_oauth2_schema)],user: UpdateUser, db: Session = Depends(get_db)):    
    
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("email")
    user_id: str = payload.get("id")

    user_model =  db.query(models.User).filter(models.User.id == user_id).first()  
    
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {user_id} does not exists")
    
    
    if user.phone_number != None:
       user_model.phone_number = user.phone_number

    if user.date_birth != None:
       user_model.date_birth = user.date_birth

    if user.home_address != None:
       user_model.home_address  = user.home_address 

    db.add(user_model)
    db.commit()
         
    return user      

@app.get("/verify/{email_verification_code}",tags=["UserRoutes"])
def verify_user_email(background_tasks: BackgroundTasks,email_verification_code: str = Path (description= "Email verification code"), db: Session = Depends(get_db)):
    user_model =  db.query(models.User).filter(models.User.email_verification_code == email_verification_code).first()  
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: invalid verification code")

    user_model.is_verified =True
    db.add(user_model)
    background_tasks.add_task(mail.send_email, user_model.email, "Thank you", "Your email has been verified! ")
    db.commit()
    return "Thanks your email has been verified"


@app.get("/user",tags=["AdminRoutes"])
def get_all_users(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], db: Session = Depends(get_db)):
    return db.query(models.User).all()


