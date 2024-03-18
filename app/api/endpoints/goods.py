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


@goods_router.get("/all")
def get_all_goods(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.in_store == True).all()
    if not products:
        return {"message": "No products found in store"}
    return {"our products": products}


@goods_router.get('/{product_id}')
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    id_list = [int(item[0]) for item in db.query(Product.id).all()]
    if product_id in id_list:
        return db.query(Product).filter(Product.id == product_id).first()
    else:
        return {"message": f"product with id {product_id} not found"}


@goods_router.post('/new')
def create_new_product(product: PyProduct, db: Session = Depends(get_db)):
    new_product = Product(title=product.title, description=product.description, in_store=True, quantity=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "new product added"}
