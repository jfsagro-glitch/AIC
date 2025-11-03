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

# Проверка структуры URL
try:
    from urllib.parse import urlparse
    parsed = urlparse(DATABASE_URL)
    if not parsed.hostname:
        raise ValueError("DATABASE_URL missing hostname")
    if not parsed.port or parsed.port <= 0 or parsed.port > 65535:
        raise ValueError(f"Invalid port in DATABASE_URL: {parsed.port}")
    if not parsed.path or parsed.path == '/':
        raise ValueError("DATABASE_URL missing database name")
except Exception as e:
    raise ValueError(
        f"Invalid DATABASE_URL format: {str(e)}\n"
        f"Current value: '{DATABASE_URL[:50]}...' (truncated)\n"
        "Expected format: 'postgresql://user:password@hostname:5432/database'\n"
        "⚠️ IMPORTANT: In Render, copy the ENTIRE 'Internal Database URL' from your PostgreSQL service.\n"
        "Make sure it includes: postgresql://, user, password, hostname, port (5432), and database name."
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
