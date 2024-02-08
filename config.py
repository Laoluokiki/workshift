from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    enviroment: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str 
    database_username: str 
    secret_key: str 
    algorithm: str 
    access_token_expiration_time: int 
    admin_email: str 
    admin_password: str 

    smtp_server :str
    smtp_port : int  
    smtp_username : str
    smtp_password : str

    remote_url: str


    class Config:
        env_file = ".env"

settings = Settings()