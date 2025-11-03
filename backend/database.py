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
    
    # Если порт не указан, добавляем порт по умолчанию для PostgreSQL (5432)
    if not parsed.port:
        # Реконструируем URL с портом по умолчанию
        if DATABASE_URL.endswith('/'):
            DATABASE_URL = DATABASE_URL.rstrip('/') + ':5432/'
        else:
            # Находим последний слэш перед именем базы данных
            if '@' in DATABASE_URL and '/' in DATABASE_URL:
                host_part = DATABASE_URL.split('@')[1].split('/')[0]
                if ':' not in host_part:
                    # Добавляем порт перед именем базы
                    DATABASE_URL = DATABASE_URL.replace(f'@{host_part}/', f'@{host_part}:5432/')
        
        # Перепарсим после добавления порта
        parsed = urlparse(DATABASE_URL)
    
    # Проверка порта
    if parsed.port and (parsed.port <= 0 or parsed.port > 65535):
        raise ValueError(f"Invalid port in DATABASE_URL: {parsed.port}")
    
    # Проверка имени базы данных
    if not parsed.path or parsed.path == '/' or parsed.path == '':
        raise ValueError("DATABASE_URL missing database name")
        
except Exception as e:
    raise ValueError(
        f"Invalid DATABASE_URL format: {str(e)}\n"
        f"Current value: '{DATABASE_URL[:80]}...' (truncated)\n"
        "Expected format: 'postgresql://user:password@hostname:5432/database'\n"
        "⚠️ IMPORTANT: In Render, copy the ENTIRE 'Internal Database URL' from your PostgreSQL service.\n"
        "Make sure it includes: postgresql://, user, password, hostname, port (5432), and database name.\n"
        "If port is missing, it will default to 5432."
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
