from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from models.transaction import Transaction


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, amount, category_id, comment=None):
        transaction = Transaction(
            amount=amount,
            category_id=category_id,
            comment=comment
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction
    
    def get_by_month(self,  month: int, year:int,):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        return self.db.query(Transaction).filter(
            Transaction.created_at >= start,
            Transaction.created_at < end
        ).options(joinedload(Transaction.category)).all()
    
    def get_all(self):
        return self.db.query(Transaction).options(joinedload(Transaction.category)).all()