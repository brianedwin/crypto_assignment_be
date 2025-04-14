from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
    id_number: str

class UserLogin(BaseModel):
    username: str
    password: str
    otp_code: str

class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str
