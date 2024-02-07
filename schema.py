from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date, timedelta, timezone


class User(BaseModel): 
    name : str = Field(min_lenghts=3)
    phone_number : str = Field(min_lenghts=10)
    email: EmailStr
    date_birth : str = Field(min_lenghts=6) 
    home_address : str = Field(min_lenghts=6)
    marital_status : Optional[str] = None

class UpdateUser(BaseModel):
    name : str = Field(min_lenghts=3)
    phone_number : str = Field(min_lenghts=10)
    email: EmailStr
    date_birth : str = Field(min_lenghts=6) 
    home_address : str = Field(min_lenghts=6)
    marital_status : Optional[str] = None
    

class Admin(BaseModel):
    username : str
    email : EmailStr
    disabled : bool | None = None
    password : str

class UpdateAdmin(BaseModel):
    username : str
    email : EmailStr
    disabled : bool | None = None
    password : str

class Department(BaseModel):
    name_of_department: str

class UpdateDepartment(BaseModel):
   name_of_department : str

class Role(BaseModel):
    department_id : str
    name_of_role : str
    describe_role : str
    minimum_hour : int
    maximum_hour : int   

class UpdateRole(BaseModel):
    department_id : str
    name_of_role : str
    describe_role : str
    minimum_hour : int
    maximum_hour : int   

class Shift(BaseModel):
    role_id : int
    no_of_resources : int
    start_time : int
    end_time : int
    date_created : date

class UpdateShift(BaseModel):   
    role_id : int
    no_of_resources : int
    start_time : int
    end_time : int
    date_created: date

class Usershift(BaseModel):
    user_id : int
    shift_id : int
    date_created : date 

class UpdateUsershift(BaseModel):
    user_id : int
    shift_id : int
    date_created : date

class Token(BaseModel):
    access_token: str
    token_type: str    
        


