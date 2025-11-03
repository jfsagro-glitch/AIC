from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import aiohttp
import os
from dotenv import load_dotenv
import json

load_dotenv()

router = APIRouter()

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class ConversationRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {}

class ParameterEstimationRequest(BaseModel):
    property_type: str
    available_data: Dict[str, Any]
    missing_params: List[str]

class ValidationRequest(BaseModel):
    property_type: str
    property_data: Dict[str, Any]
    calculation_details: Dict[str, Any]

async def call_deepseek(prompt: str) -> str:
    """Вызов DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY не настроен")
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Ты эксперт по оценке коммерческой недвижимости. Отвечай четко и структурированно, используя формат JSON когда это уместно."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"DeepSeek API error: {error_text}"
                    )
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при вызове DeepSeek API: {str(e)}")

@router.post("/conversation")
async def ai_conversation(request: ConversationRequest):
    """Общение с AI ассистентом"""
    try:
        # Формирование промпта с контекстом
        context_str = json.dumps(request.context, ensure_ascii=False, indent=2) if request.context else "Контекст не предоставлен"
        
        prompt = f"""Пользователь задал вопрос об оценке недвижимости: {request.message}

Контекст объекта недвижимости:
{context_str}

Ответь на вопрос пользователя, используя предоставленный контекст. Если контекст содержит данные об объекте, используй их в ответе.
Если пользователь просит оценить или скорректировать параметры, предоставь ответ в формате JSON с ключами для каждого параметра."""
        
        response = await call_deepseek(prompt)
        
        # Попытка извлечь JSON из ответа если он есть
        updated_parameters = None
        try:
            # Ищем JSON в ответе
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                updated_parameters = json.loads(json_match.group())
        except:
            pass
        
        return {
            "response": response,
            "updated_parameters": updated_parameters
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estimate-parameters")
async def estimate_parameters(request: ParameterEstimationRequest):
    """Оценка недостающих параметров с помощью AI"""
    try:
        from ai_core.constants import PROMPT_TEMPLATES
        
        prompt = PROMPT_TEMPLATES["parameter_estimation"].format(
            property_type=request.property_type,
            available_data=json.dumps(request.available_data, ensure_ascii=False),
            missing_params=", ".join(request.missing_params)
        )
        
        response = await call_deepseek(prompt)
        
        # Извлечение JSON из ответа
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if json_match:
            estimated_params = json.loads(json_match.group())
        else:
            estimated_params = {}
        
        return {
            "success": True,
            "estimated_parameters": estimated_params,
            "ai_response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def validate_calculation(request: ValidationRequest):
    """Валидация расчета стоимости с помощью AI"""
    try:
        from ai_core.constants import PROMPT_TEMPLATES
        
        prompt = PROMPT_TEMPLATES["validation"].format(
            property_type=request.property_type,
            property_data=json.dumps(request.property_data, ensure_ascii=False),
            calculation_details=json.dumps(request.calculation_details, ensure_ascii=False)
        )
        
        response = await call_deepseek(prompt)
        
        # Извлечение JSON из ответа
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if json_match:
            validation_result = json.loads(json_match.group())
            # Убеждаемся что есть нужные поля
            if "is_valid" not in validation_result:
                validation_result["is_valid"] = True
            if "needs_correction" not in validation_result:
                validation_result["needs_correction"] = False
            if "recommendations" not in validation_result:
                validation_result["recommendations"] = []
            if "confidence_score" not in validation_result:
                validation_result["confidence_score"] = 0.8
        else:
            validation_result = {
                "is_valid": True,
                "needs_correction": False,
                "recommendations": [],
                "confidence_score": 0.7
            }
        
        return {
            "success": True,
            "validation": validation_result,
            "ai_response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
