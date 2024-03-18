import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.models.goods import PyProduct
from app.api.db.database import get_db
from app.api.db.models import User, Product
from app.core.security import authenticate_user, create_access_token, get_current_user, get_password_hash

goods_router = APIRouter(prefix="/goods")
security = HTTPBasic()


@goods_router.get("/all/")
def get_all_goods(db: Session = Depends(get_db)):
    products = db.query(Product.id, Product.title).filter(Product.in_store == True).all()
    if not products:
        return {"message": "No products found in store"}
    return {"our products": products}
