from fastapi import FastAPI, Path, Depends 
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from routes import admin, user, department, shift, userrole
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


origins = [
    "https://workshift-frontend-1ja6f0rtq-olaoluwas-projects-a9f0ed67.vercel.app",
    "http://localhost:4200", 
    "https://workshift-frontend.vercel.app",
    "https://happy-smoke-04b222310.3.azurestaticapps.net"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS","PUT"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse("""
                <!-- templates/base.html -->
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Colonees Team AI API</title>
                <style>
                    body {
                        font-family: 'Roboto', sans-serif;
                        margin: 40px;
                        text-align: center;
                        background-color: #f7f7f7;
                    }
                    h1 {
                        font-size: 2.5em;
                        color: #333;
                    }
                    p {
                        font-size: 1.2em;
                        color: #555;
                    }
                    footer {
                        margin-top: 20px;
                        font-size: 0.8em;
                        color: #777;
                    }
                </style>
            </head>
            <body>
                <h1> WELCOME TO WORK_SHIFT_PROJECT BY ABAYOMI </h1>
               
            </body>
            </html>
        """)

app.include_router(admin.app)
app.include_router(user.app)
app.include_router(department.app)
app.include_router(shift.app)
app.include_router(userrole.app)
