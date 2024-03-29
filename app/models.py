from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    points = Column(JSONB, nullable=False)
