from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.api.models.user import UserToRegister, UserToLogin
from app.api.db.database import get_db
from app.api.db.models import User
from app.core.security import authenticate_user, create_access_token, get_user, get_password_hash


user_router = APIRouter(prefix="/auth")
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")


@user_router.get("/register/")
def show_register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@user_router.post("/register/")
def register_user(request: Request, username: str = Form(...), full_name: str = Form(), email: str = Form(...),
                  password: str = Form(...), password_repeat: str = Form(...), db: Session = Depends(get_db)):
    if request.method == "POST":
        existing_user = get_user(username, db)
        if existing_user:
            return {"message": "user with the same username already exists"}
        else:
            used_email = db.query(User).filter(User.email == email).first()
            if used_email:
                return {"message": "this email is already used"}
            else:
                if password != password_repeat:
                    return {"message": "passwords are different"}
                else:
                    db_user = User(username=username, full_name=full_name, email=email, hashed_password=get_password_hash(password))
                    db.add(db_user)
                    db.commit()
                    db.refresh(db_user)
                    return templates.TemplateResponse("suc_reg.html", {"request": request, "user_created": db_user})


@user_router.post("/login/")
def login_user(user: UserToLogin):
    username = user.username
    password = user.password
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}