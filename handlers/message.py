from aiogram import Router
from aiogram.types import Message
from filters.auth_filter import IsAuthorized
from services.expense_service import parser, category_track
from db.database import SessionLocal
from repositories.transaction_repository import TransactionRepository
from models.category import OperationType
from services.timezone_service import to_local

router = Router()

@router.message(IsAuthorized())
async def handle_expense(message: Message) -> None:
    db = SessionLocal()
    try:
        repo_trans = TransactionRepository(db)
        pars = parser(message.text)
        operation, amount, category_name, comment = pars
        category_track(db, operation = operation, amount= amount, category_name=category_name, comment=comment)
        transactions = repo_trans.get_last_ten()
        lines = []
        lines.append("Транзакция добавлена")
        lines.append("--------------------")
        for transaction in reversed(transactions):
            date_str = to_local(transaction.created_at).strftime("%d.%m %H:%M")
            if transaction.category.type == OperationType.income:
                lines.append(f"{date_str} | {transaction.category.name} | +{transaction.amount} | {transaction.comment}")
            else: lines.append(f"{date_str} | {transaction.category.name} | -{transaction.amount} | {transaction.comment}")
        text = "\n".join(lines)
        await message.answer(text)


    except ValueError as e: 
        await message.answer(str(e))
    finally:
        db.close()