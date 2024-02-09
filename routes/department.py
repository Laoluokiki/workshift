
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from sqlalchemy.orm import Session
import models,oauth2
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from schema import Department,UpdateDepartment,Role,UpdateRole
from typing import Annotated




app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-dept", tags=["AdminRoutes"])
def create_dept(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], department: Department,  db: Session = Depends(get_db)):
    department_model = db.query(models.Departments).filter(
        models.Departments.name_of_department == department.name_of_department).first()
    if department_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Department: {department.name_of_department} is  already created")

    department_model = models.Departments(**department.model_dump())

    db.add(department_model)
    db.commit()

    return department

@app.put("/update-dept", tags=["AdminRoutes"])
def update_dept(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)],update_dept :str, department : UpdateDepartment, db: Session = Depends(get_db)):    
    department_model =  db.query(models.Departments).filter(models.Departments.name_of_department == department.name_of_department).first()  
    
    if department_model is  None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"message: {department.name_of_department} does not exists")

    db.add(department_model)
    db.commit()
         
    return department        
    

@app.get("/departments", tags=["AdminRoutes"])
def get_all_departments(db: Session = Depends(get_db)):
    return db.query(models.Departments).all()


@app.post("/create-roles", tags=["AdminRoutes"])
def create_role(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)],role: Role,  db: Session = Depends(get_db)):
    #check if department exist
    department_model = db.query(models.Departments).filter(
        models.Departments.id  == role.department_id ).first()

    if department_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"mesage: Department {role.department_id} does not exist")

    # check if role has been created 
    role_model = db.query(models.Roles).filter(
        models.Roles.department_id  == role.department_id, models.Roles.name_of_role==role.name_of_role).first()
    
    if role_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"mesage: Role  {role.name_of_role} already exist")
    
    role_model = models.Roles(**role.model_dump())

    db.add(role_model)
    db.commit()

    return role

@app.put("/update-roles", tags=["AdminRoutes"])
def update_roles(token: Annotated[str, Depends(oauth2.admin_oauth2_schema)], role_id :str, role : UpdateRole, db: Session = Depends(get_db)):    
    role_model =  db.query(models.Roles).filter(models.Roles.id == role_id).first()  
    
    if role_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role: {role_id} does not exists")
    
    if role.name_of_role != None:
        role_model.name_of_role = role.name_of_role

    if role.describe_role != None:       
       role_model.describe_role =  role.describe_role
    
    if role.department_id != None:       
       role_model.department_id =  role.department_id

    if role.minimum_hour != None:
       role_model.minimum_hour = role.minimum_hour

    if role.maximum_hour != None:
       role_model.maximum_hour = role.maximum_hour    

    db.add(role_model)
    db.commit()
         
    return role          

@app.get("/roles", tags=["AdminRoutes"])
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(models.Roles).all()

 







