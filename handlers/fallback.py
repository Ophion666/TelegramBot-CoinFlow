from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def fallback_handler(message: Message) -> None:
    await message.answer(" Ввел что то что бот не умеет или Не авторизован. Введи /login")