import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.users import user_router, users_router
from app.api.endpoints.goods import goods_router
from pages.router import router as router_pages

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_main():
    return {"message": "Welcome to the best online store"}

app.include_router(user_router)
app.include_router(users_router)
app.include_router(goods_router)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)