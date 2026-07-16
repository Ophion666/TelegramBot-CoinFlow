from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from db.database import SessionLocal
from filters.auth_filter import IsAuthorized
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from repositories.transaction_repository import TransactionRepository
from services.statistics_service import aggregate, calculate_percentages

class StatsStates(StatesGroup):
    waiting_for_period = State()

router = Router()

@router.message(Command("stats"), IsAuthorized())
async def stats_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введи месяц в формате 'мм.гггг' или слова 'все'")
    await state.set_state(StatsStates.waiting_for_period)

@router.message(StateFilter(StatsStates.waiting_for_period))
async def period_handler(message: Message, state: FSMContext) -> None:
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
        
        stats = aggregate(transactions)
        percentages = calculate_percentages(stats["category_totals"], stats["total_expense"])
        income_percentages = calculate_percentages(stats["income_category_totals"], stats["total_income"])

        lines = []

        lines.append("Доходы:")
        for category_name, amount in stats["income_category_totals"].items():
            inc_perc = income_percentages.get(category_name, 0)
            lines.append(f"{category_name} - {amount} ({inc_perc}%)")
        lines.append(f"Итого доход: {stats['total_income']}")

        lines.append("----------")

        lines.append("Расходы:")
        for category_name, amount in stats["category_totals"].items():
            percent = percentages.get(category_name, 0)
            lines.append(f"{category_name} - {amount} ({percent}%)")
        lines.append(f"Итого расход: {stats['total_expense']}")

        lines.append("----------")
        raznica = stats["total_income"] - stats["total_expense"]
        lines.append(f"Разница: {raznica}")
        

        text = "\n".join(lines)
        await message.answer(text)
        await state.clear()
    
    except ValueError:
        await message.answer("Неверный формат. Введи ММ.ГГГГ или слово 'все'")
    finally:
        db.close()