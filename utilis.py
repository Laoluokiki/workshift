import secrets
import time 
import typing

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password:str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# For OTPs

def generate_otp(length=6):
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(length))
    return otp


def generate_timed_otp(expiration_minutes=1):
    otp = generate_otp()
    current_time = int(time.time())
    expiration_time = current_time + (expiration_minutes * 60)
    otp_data = (otp, expiration_time)
    return otp_data


def validate_otp(otp_data):
    otp, expiration_time = otp_data
    current_time = int(time.time())

    # Check if the OTP has expired
    if current_time > expiration_time:
        return False, "OTP has expired"

    # Add additional validation logic here if needed

    return True, "OTP is valid"
