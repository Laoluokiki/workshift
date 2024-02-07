
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Department,UpdateDepartment,Role,UpdateRole



app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-dept")
def create_dept(department: Department,  db: Session = Depends(get_db)):
    department_model = db.query(models.Departments).filter(
        models.Departments.name_of_department == department.name_of_department).first()
    if department_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Department: {department.name_of_department} is  already created")

    department_model = models.Departments(**department.model_dump())

    db.add(department_model)
    db.commit()

    return department

@app.put("/update-dept")
def update_admin(update_dept :str, department : UpdateDepartment, db: Session = Depends(get_db)):    
    department_model =  db.query(models.Departments).filter(models.Departments.name_of_department == department.name_of_department).first()  
    
    if department_model is  None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {department.name_of_department} does not exists")

    db.add(department_model)
    db.commit()
         
    return department        
    

@app.get("/departments")
def get_all_departments(db: Session = Depends(get_db)):
    return db.query(models.Departments).all()


@app.post("/create-roles")
def create_role(role: Role,  db: Session = Depends(get_db)):
    role_model = db.query(models.Roles).filter(
        models.Roles.department_id  == role.department_id ).first()

    if role_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"mesage: {department.name_of_department} is  already created")

    role_model = models.Roles(**role.model_dump())

    db.add(role_model)
    db.commit()

    return role

@app.put("/update-roles")
def update_roles(role_id :str, role : UpdateRole, db: Session = Depends(get_db)):    
    role_model =  db.query(models.Roles).filter(models.Roles.id == role_id).first()  
    
    if role_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role: {role_id} does not exists")
    
    if role.name_of_role != None:
        role_model.name_of_role = role.name_of_role

    if role.describe_role != None:       
       role_model.describe_role =  role.describe_role

    if role.minimum_hour != None:
       role_model.minimum_hour = role.minimum_hour

    if role.maximum_hour != None:
       role_model.maximum_hour = role.maximum_hour    

    db.add(role_model)
    db.commit()
         
    return role          

@app.get("/roles")
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(models.Roles).all()









