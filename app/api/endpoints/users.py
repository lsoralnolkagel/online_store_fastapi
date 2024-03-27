from fastapi import APIRouter, Depends, Request, responses, HTTPException, Form, Header
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.models.user import UserToRegister, UserToLogin
from app.api.db.database import get_db
from app.api.db.models import User
from app.core.security import authenticate_user, get_current_user, create_access_token, get_user, get_password_hash


user_router = APIRouter(prefix="/auth")
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.get("/register")
def show_register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@user_router.post("/register")
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


@user_router.get("/login")
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@user_router.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    if request.method == "POST":
        if not authenticate_user(username, password):
            return templates.TemplateResponse("error.html", {"request": request})
        access_token = create_access_token(data={"sub": username})
        response = templates.TemplateResponse("suc_log.html", {"request": request, "token": access_token, "token_type": "Bearer"})
        response.set_cookie(key="access_token", value=access_token)
        return response


@user_router.get("/logout")
def logout_user(request: Request):
    response = templates.TemplateResponse("logout.html", {"request": request})
    response.delete_cookie(key="access_token")
    return response


users_router = APIRouter(prefix="/users")


@users_router.get("/me")
def get_my_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('access_token')
    current_user = get_current_user(token, db)
    if current_user:
        return templates.TemplateResponse("my_page.html", {"request": request, "user": current_user})
    else:
        return templates.TemplateResponse("error.html", {"request": request})


@users_router.get("/{id}")
def get_user_by_id(request: Request, id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return templates.TemplateResponse("users_page.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("user_error.html", {"request": request})