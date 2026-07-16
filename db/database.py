from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data/finance.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
