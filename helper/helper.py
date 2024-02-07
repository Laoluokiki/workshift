from database import engine,SessionLocal


def get_db():
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()  