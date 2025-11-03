from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in Render dashboard: Settings → Environment Variables"
    )

# Проверка формата DATABASE_URL
if not DATABASE_URL.startswith(('postgresql://', 'postgres://')):
    raise ValueError(
        f"Invalid DATABASE_URL format: '{DATABASE_URL}'. "
        "Expected format: 'postgresql://user:password@host:port/database'\n"
        "In Render: Use the FULL Internal Database URL from your PostgreSQL service, "
        "not just the database name. Go to your PostgreSQL service → "
        "Copy 'Internal Database URL' (not External URL)"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
