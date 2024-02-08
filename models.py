from sqlalchemy import Column, Integer, String, Float, Boolean, Date, TIMESTAMP, text
from database import Base
from sqlalchemy.sql import func


class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True, index=True)
   first_name = Column(String)
   last_name = Column(String)
   gender = Column(String)
   phone_number  = Column(String, nullable=False, unique=True)
   email = Column(String, nullable=False, unique=True)
   date_birth = Column(Date)
   home_address = Column(String)
   marital_status = Column(String)
   password = Column(String)
   email_verification_code = Column(String)
   is_verified = Column(Boolean, default=False)
   date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())



class Admin(Base):
   __tablename__ = "admin"
   id = Column(Integer, primary_key=True, index=True)
   username = Column(String, nullable=False, unique=True)
   email = Column(String, nullable=False, unique=True)
   disabled = Column(Boolean)
   password = Column(String)
   date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class  Departments(Base):
   __tablename__ = "departments"
   id = Column(Integer, primary_key=True, index=True)
   name_of_department = Column(String)
   date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(String) 
    name_of_role = Column(String, nullable=False, unique=True)
    describe_role = Column(String)
    minimum_hour =  Column(Integer)
    maximum_hour =  Column(Integer)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, index=True)
    role_id =  Column(Integer)
    no_of_resources = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    date_created = Column(Date)

class Usershift(Base):
    __tablename__ = "user_shifts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    shift_id = Column(Integer)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    role_id = Column(Integer)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
   
    