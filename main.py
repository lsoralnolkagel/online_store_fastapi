import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.api.endpoints.users import user_router, users_router
from app.api.endpoints.goods import goods_router
from app.api.db.database import get_db
from app.api.db.models import Product
from pages.router import router as router_pages

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def get_main(request: Request, db: Session = Depends(get_db)):
    goods = db.query(Product).filter(Product.in_store == True).limit(5)
    return templates.TemplateResponse("main_page.html", {"request": request, "goods": goods})


app.include_router(user_router)
app.include_router(users_router)
app.include_router(goods_router)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)