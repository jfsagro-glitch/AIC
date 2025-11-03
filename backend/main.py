from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from routers import valuation, ai, files, history, market
from database import engine, Base

load_dotenv()

app = FastAPI(
    title="AI Залоговик API",
    description="Система автоматизированной оценки коммерческой недвижимости",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц БД
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(valuation.router, prefix="/api/valuation", tags=["valuation"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(market.router, prefix="/api/market", tags=["market"])

@app.get("/")
async def root():
    return {"message": "AI Залоговик API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}
