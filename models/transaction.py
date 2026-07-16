from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    amount = Column(Float, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    comment = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category")