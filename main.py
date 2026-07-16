from db.database import Base, engine

from models import category
from models import transaction
from models import authorized_user
from services import expense_service
from services import statistics_service
from db.database import SessionLocal
import asyncio
from bot.bot import bot, dp

db = SessionLocal()

Base.metadata.create_all(bind=engine)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())