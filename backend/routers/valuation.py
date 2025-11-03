from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os

# Импорт из локального ai_core (копия в backend)
from ai_core.calculations import (
    direct_capitalization, dcf_valuation,
    CommercialProperty, Hotel, ShoppingCenter, OfficeCenter,
    CapitalizationResult, DCFResult
)
from models import ValuationResult, ValuationRecord as ValuationRecordDB
from database import get_db

router = APIRouter()

@router.post("/calculate")
async def calculate_valuation(
    property_data: dict,
    method: str = "direct_capitalization",
    db: Session = Depends(get_db)
):
    """
    Расчет стоимости недвижимости
    method: "direct_capitalization" или "dcf"
    """
    try:
        # Определение типа объекта и создание соответствующей модели
        property_type = property_data.get("property_type")
        
        # Преобразование строки даты в datetime если нужно
        if "assessment_date" in property_data and isinstance(property_data["assessment_date"], str):
            from dateutil.parser import parse as parse_date
            property_data["assessment_date"] = parse_date(property_data["assessment_date"])
        
        # Установка cap_rate по умолчанию если не указан
        if "cap_rate" not in property_data:
            property_data["cap_rate"] = 0.1  # Значение по умолчанию
        
        if property_type == "hotel":
            property = Hotel(
                rooms_count=property_data.get("rooms_count", 0),
                hotel_category=property_data.get("hotel_category", "3 звезды"),
                adr=property_data.get("adr", 0),
                **{k: v for k, v in property_data.items() 
                   if k not in ["rooms_count", "hotel_category", "adr"]}
            )
        elif property_type == "shopping_center":
            property = ShoppingCenter(
                current_lease_area=property_data.get("current_lease_area", 0),
                base_rent_income=property_data.get("base_rent_income", 0),
                operation_rate_income=property_data.get("operation_rate_income", 0),
                marketing_fee_income=property_data.get("marketing_fee_income", 0),
                **{k: v for k, v in property_data.items() 
                   if k not in ["current_lease_area", "base_rent_income", 
                               "operation_rate_income", "marketing_fee_income"]}
            )
        elif property_type == "office_center":
            property = OfficeCenter(
                class_type=property_data.get("class_type", "B"),
                condition=property_data.get("condition", "хорошее"),
                rent_rate_per_sqm=property_data.get("rent_rate_per_sqm", 0),
                **{k: v for k, v in property_data.items() 
                   if k not in ["class_type", "condition", "rent_rate_per_sqm"]}
            )
        else:
            property = CommercialProperty(**property_data)
        
        # Расчет в зависимости от метода
        if method == "direct_capitalization":
            cap_result = direct_capitalization(property)
            result = ValuationResult(
                property_type=property_type,
                property_value=cap_result.property_value,
                calculation_method=method,
                capitalization_result=cap_result,
                calculation_date=datetime.now()
            )
        elif method == "dcf":
            discount_rate = property_data.get("discount_rate", 0.12)
            dcf_result = dcf_valuation(property, years=5, discount_rate=discount_rate)
            result = ValuationResult(
                property_type=property_type,
                property_value=dcf_result.total_value,
                calculation_method=method,
                dcf_result=dcf_result,
                calculation_date=datetime.now()
            )
        else:
            raise HTTPException(status_code=400, detail=f"Неизвестный метод расчета: {method}")
        
        # Сохранение в БД
        record = ValuationRecordDB(
            property_type=property_type,
            property_data=property_data,
            calculation_method=method,
            result=result.dict()
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return {
            "success": True,
            "result": result.dict(),
            "record_id": record.id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
