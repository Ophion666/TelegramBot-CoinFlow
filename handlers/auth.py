from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from repositories.authorized_user_repository import AuthorizedUserRepository
from config import PIN_CODE
from db.database import SessionLocal


router = Router()

class AuthStates(StatesGroup):
    waiting_for_pin = State()

@router.message(Command("login"))
async def login_handler(message: Message, state: FSMContext) -> None:
    db = SessionLocal()
    try:
        auth_repo = AuthorizedUserRepository(db)
        telega_id = message.from_user.id
        auth = auth_repo.exists(telegram_id=telega_id)
        if auth:
            await message.answer("Уже авторизован")
        else: 
            await message.answer("Введи ПИН")
            await state.set_state(AuthStates.waiting_for_pin)
    finally:
        db.close()

@router.message(StateFilter(AuthStates.waiting_for_pin))
async def pin_handler(message: Message, state:FSMContext) -> None:
    db = SessionLocal()
    try:
        register_repo = AuthorizedUserRepository(db)
        if message.text == PIN_CODE:
            telega_id = message.from_user.id
            register = register_repo.create(telegram_id=telega_id)
            await state.clear()
            await message.answer("Авторизован")
        else: await message.answer("Не верный пин)")
    finally:
        db.close()
