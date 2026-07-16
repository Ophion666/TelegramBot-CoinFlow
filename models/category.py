from enum import Enum

from sqlalchemy import Column, Enum as SqlEnum, Integer, String

from db.database import Base


class OperationType(str, Enum):
    income = "income"
    expense = "expense"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(SqlEnum(OperationType), nullable=False)