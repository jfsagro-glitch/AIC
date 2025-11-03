from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
import sys
import json

# Импорт функции из модуля ai
sys.path.append(os.path.dirname(__file__))
from ai import call_deepseek

router = APIRouter()

class MarketDataRequest(BaseModel):
    property_type: str
    location: str

@router.get("/data")
async def get_market_data(property_type: str, location: str = "Россия"):
    """
    Получение рыночных данных через AI
    """
    try:
        from ai_core.constants import PROMPT_TEMPLATES
        
        prompt = PROMPT_TEMPLATES["market_data"].format(
            type=property_type,
            location=location
        )
        
        response = await call_deepseek(prompt)
        
        # Попытка извлечь JSON из ответа
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if json_match:
            market_data = json.loads(json_match.group())
        else:
            # Если JSON не найден, возвращаем текстовый ответ
            market_data = {"raw_response": response}
        
        return {
            "success": True,
            "property_type": property_type,
            "location": location,
            "market_data": market_data,
            "ai_response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
