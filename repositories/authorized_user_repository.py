from sqlalchemy.orm import Session
from models.authorized_user import AuthorizedUser

class AuthorizedUserRepository:
    def __init__(self, db: Session):
        self.db = db


    def exists(self, telegram_id: int) -> bool:
        return self.db.query(AuthorizedUser).filter(AuthorizedUser.telegram_id == telegram_id).first() is not None
    
    def create(self, telegram_id: int) -> AuthorizedUser:
        user = AuthorizedUser(
            telegram_id = telegram_id,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user