from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from database import Base

class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   phone_number  = Column(String)
   email = Column(String)
   date_birth = Column(String)
   home_address = Column(String)
   marital_status = Column(String)

class Admin(Base):
   __tablename__ = "admin"
   id = Column(Integer, primary_key=True, index=True)
   username = Column(String)
   email = Column(String)
   disabled = Column(Boolean)
   password = Column(String)

class  Departments(Base):
   __tablename__ = "department"
   id = Column(Integer, primary_key=True, index=True)
   name_of_department = Column(String)

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(String) 
    name_of_role = Column(String)
    describe_role = Column(String)
    minimum_hour =  Column(Integer)
    maximum_hour =  Column(Integer)

class Shift(Base):
    __tablename__ = "creating shifts"
    id = Column(Integer, primary_key=True, index=True)
    role_id =  Column(Integer)
    no_of_resources = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    date_created = Column(Date)

class Usershift(Base):
    __tablename__ = "shifts by users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    shift_id = Column(Integer)
    date_created = Column(Date)
    

   
    