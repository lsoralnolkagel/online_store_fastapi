from pydantic import BaseModel


class PyProduct(BaseModel):
    title: str
    description: str


class ProductInStore(BaseModel):
    id: int
    title: str
    in_store: bool
    quantity: int
