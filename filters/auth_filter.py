from aiogram.filters import BaseFilter
from aiogram.types import Message
from db.database import SessionLocal
from repositories.authorized_user_repository import AuthorizedUserRepository

class IsAuthorized(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        db = SessionLocal()
        try:
            auth_repo = AuthorizedUserRepository(db)
            return auth_repo.exists(message.from_user.id)
        finally:
            db.close()
