from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from db.database import SessionLocal
from filters.auth_filter import IsAuthorized
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from repositories.transaction_repository import TransactionRepository
from models.category import OperationType

class HistoryStates(StatesGroup):
    waiting_for_period = State()

router = Router()

@router.message(Command("his"), IsAuthorized())
async def history_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введи месяц в формате 'мм.гггг'")
    await state.set_state(HistoryStates.waiting_for_period)

@router.message(StateFilter(HistoryStates.waiting_for_period))
async def history_period_handler(message: Message, state: FSMContext) -> None:
    text = message.text.strip().lower()
    db = SessionLocal()
    try:
        transaction_repo = TransactionRepository(db)
        if text == "все":
            transactions = transaction_repo.get_all()
        else:
            new_text = text.split(".")
            resault = [int(x) for x in new_text]
            month, year = resault
            transactions = transaction_repo.get_by_month(month, year)

        lines = []
        for transaction in transactions:
            date_str = transaction.created_at.strftime("%d.%m.%Y")
            if transaction.category.type == OperationType.income:
                lines.append(f"{date_str} | {transaction.category.name} | +{transaction.amount} | {transaction.comment}")
            else: lines.append(f"{date_str} | {transaction.category.name} | -{transaction.amount} | {transaction.comment}")

        text = "\n".join(lines)
        await message.answer(text)
        await state.clear()
    except ValueError:
        await message.answer("Неверный формат. Введи ММ.ГГГГ")
    finally:
        db.close()