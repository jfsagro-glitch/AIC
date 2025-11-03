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
        if '@' in DATABASE_URL and '/' in DATABASE_URL:
            # Находим хост (часть после @ и до /)
            parts = DATABASE_URL.split('@', 1)
            if len(parts) == 2:
                auth_part = parts[0]
                host_db_part = parts[1]
                
                # Разделяем хост и базу данных
                if '/' in host_db_part:
                    host_part, db_part = host_db_part.split('/', 1)
                    # Если в хосте нет порта, добавляем
                    if ':' not in host_part:
                        DATABASE_URL = f"{auth_part}@{host_part}:5432/{db_part}"
                    else:
                        # Порт уже есть, но не распарсился - возможно проблема с форматом
                        pass
                else:
                    # Нет слеша после хоста - добавляем порт и слэш
                    DATABASE_URL = f"{auth_part}@{host_db_part}:5432/"
        
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
