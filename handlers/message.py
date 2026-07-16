from aiogram import Router
from aiogram.types import Message
from filters.auth_filter import IsAuthorized
from services.expense_service import parser, category_track
from db.database import SessionLocal

router = Router()

@router.message(IsAuthorized())
async def handle_expense(message: Message) -> None:
    db = SessionLocal()
    try:
        pars = parser(message.text)
        operation, amount, category_name, comment = pars
        category_track(db, operation = operation, amount= amount, category_name=category_name, comment=comment)
        await message.answer("Транзакция добавлена")
    except ValueError as e: 
        await message.answer(str(e))
    finally:
        db.close()