from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.api.db.database import Base, engine


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    in_store: Mapped[bool]
    quantity: Mapped[int] = mapped_column(BigInteger, nullable=False)


Base.metadata.create_all(bind=engine)