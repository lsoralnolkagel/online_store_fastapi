import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.models.user import UserToRegister, UserToLogin
from app.api.db.database import get_db
from app.api.db.models import User
from app.core.security import authenticate_user, create_access_token, get_current_user, get_password_hash


user_router = APIRouter(prefix="/auth")
security = HTTPBasic()


@user_router.post("/register/")
def register_user(user: UserToRegister, db: Session = Depends(get_db)):
    db_user = User(username=user.username, full_name=user.full_name, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user created": db_user}


@user_router.post("/login/")
def login_user(user: UserToLogin):
    username = user.username
    password = user.password
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}