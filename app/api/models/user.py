from pydantic import BaseModel


class UserToRegister(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserInDB(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str


class UserToLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str