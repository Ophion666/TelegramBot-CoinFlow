from sqlalchemy.orm import Session

from models.category import Category, OperationType


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str):
        return self.db.query(Category).filter(Category.name == name).first()

    def create(self, name: str, operation_type: OperationType):
        category = Category(
            name=name,
            type=operation_type
        )

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category