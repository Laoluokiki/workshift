from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException

from typing import Annotated

from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

SECRET_KEY = "21d7f0f4f33ed08a8d28a59abab8b56a373342a50b7f549877436fb9922ce38b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email: str =  payload.get("email")

        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email = email,is_authenticated=True)
    
    except JWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    return verify_access_token(token,credentials_exception)
    
    


