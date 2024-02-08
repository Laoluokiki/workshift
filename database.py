from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

# local enviroment
DATABASE_URL = "sqlite:///./workshift.db"
engine_dev = create_engine(
    DATABASE_URL, connect_args={"check_same_thread":False}
)

#production enviroment
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine_production = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'sslmode':'require'})  


if settings.enviroment== "dev" :
    engine = engine_dev
    print("Development enviroment")
else:
    engine = engine_production
    print("Production enviroment") 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()