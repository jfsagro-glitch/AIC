from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import ValuationRecord as ValuationRecordDB
from pydantic import BaseModel

router = APIRouter()

class HistoryItem(BaseModel):
    id: int
    property_type: str
    property_data: dict
    calculation_method: str
    result: dict
    created_at: datetime

@router.get("/")
async def get_history(
    limit: int = 50,
    offset: int = 0,
    property_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получение истории расчетов"""
    query = db.query(ValuationRecordDB)
    
    if property_type:
        query = query.filter(ValuationRecordDB.property_type == property_type)
    
    records = query.order_by(ValuationRecordDB.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "count": len(records),
        "records": [
            {
                "id": r.id,
                "property_type": r.property_type,
                "property_data": r.property_data,
                "calculation_method": r.calculation_method,
                "result": r.result,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    }

@router.get("/{record_id}")
async def get_record(record_id: int, db: Session = Depends(get_db)):
    """Получение конкретного расчета"""
    record = db.query(ValuationRecordDB).filter(ValuationRecordDB.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    return {
        "success": True,
        "record": {
            "id": record.id,
            "property_type": record.property_type,
            "property_data": record.property_data,
            "calculation_method": record.calculation_method,
            "result": record.result,
            "created_at": record.created_at.isoformat() if record.created_at else None
        }
    }

@router.delete("/{record_id}")
async def delete_record(record_id: int, db: Session = Depends(get_db)):
    """Удаление записи из истории"""
    record = db.query(ValuationRecordDB).filter(ValuationRecordDB.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    db.delete(record)
    db.commit()
    
    return {"success": True, "message": "Запись удалена"}
