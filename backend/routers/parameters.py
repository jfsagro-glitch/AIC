"""
Роутер для работы с параметрами расчета ДДП
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel

router = APIRouter()


class ParameterCheckRequest(BaseModel):
    property_type: str
    property_data: Dict[str, Any]
    method: str = "dcf"


class ParameterOptionsResponse(BaseModel):
    missing_parameters: List[str]
    parameter_options: Dict[str, Any]
    suggested_values: Dict[str, Any]


# Определения обязательных параметров для каждого типа
REQUIRED_PARAMETERS = {
    "hotel": {
        "dcf": [
            "rooms_count",
            "occupancy_rate",
            "adr",
            "rent_growth_rate",
            "f_b_percentage",
            "other_revenue_percentage",
            "room_maintenance_percentage",
            "f_b_expense_percentage",
            "other_expense_percentage",
            "admin_expense_percentage",
            "marketing_expense_percentage",
            "maintenance_expense_percentage",
            "utilities_expense_percentage",
            "base_management_fee_percentage",
            "incentive_fee_percentage",
            "royalty_percentage",
            "property_tax",
            "land_payments",
            "insurance",
            "replacement_reserve_rate",
            "discount_rate",
            "terminal_cap_rate",
            "broker_commission",
            "total_area"
        ],
        "direct_capitalization": [
            "rooms_count",
            "occupancy_rate",
            "adr",
            "total_area"
        ]
    },
    "shopping_center": {
        "dcf": [
            "total_area",
            "current_lease_area",
            "base_rent_rate",
            "rent_growth_rates",
            "occupancy_rates",
            "operating_cost_per_sqm",
            "cost_growth_rates",
            "replacement_reserve_rate",
            "discount_rate",
            "terminal_cap_rate",
            "broker_commission"
        ],
        "direct_capitalization": [
            "total_area",
            "current_lease_area",
            "base_rent_income"
        ]
    },
    "office_center": {
        "dcf": [
            "total_area",
            "lease_area",
            "parking_spaces",
            "office_rent_rate",
            "parking_rate",
            "office_rent_growth",
            "parking_rent_growth",
            "occupancy_rate",
            "operating_cost_per_sqm",
            "cost_growth_rates",
            "replacement_reserve_rate",
            "discount_rate",
            "terminal_cap_rate",
            "broker_commission"
        ],
        "direct_capitalization": [
            "total_area",
            "lease_area",
            "rent_rate_per_sqm"
        ]
    }
}

# Параметры по умолчанию
DEFAULT_VALUES = {
    "hotel": {
        "occupancy_rate": 0.55,
        "rent_growth_rate": [0.03, 0.02, 0.05, 0.02, 0.02],
        "f_b_percentage": 0.25,
        "other_revenue_percentage": 0.10,
        "room_maintenance_percentage": 0.15,
        "f_b_expense_percentage": 0.35,
        "other_expense_percentage": 0.20,
        "admin_expense_percentage": 0.05,
        "marketing_expense_percentage": 0.03,
        "maintenance_expense_percentage": 0.04,
        "utilities_expense_percentage": 0.06,
        "base_management_fee_percentage": 0.03,
        "incentive_fee_percentage": 0.10,
        "royalty_percentage": 0.04,
        "property_tax": 0,
        "land_payments": 0,
        "insurance": 0,
        "replacement_reserve_rate": 0.03,
        "discount_rate": 0.12,
        "terminal_cap_rate": 0.10,
        "broker_commission": 0.01
    },
    "shopping_center": {
        "rent_growth_rates": [0, 0.02, 0.02, 0.02, 0.02],
        "occupancy_rates": [0.98, 0.98, 0.98, 0.98, 0.98],
        "operating_cost_per_sqm": 3500,
        "cost_growth_rates": [0, 0.02, 0.02, 0.02, 0.02],
        "replacement_reserve_rate": 0.03,
        "discount_rate": 0.12,
        "terminal_cap_rate": 0.10,
        "broker_commission": 0.01
    },
    "office_center": {
        "office_rent_growth": [0, 0.02, 0.02, 0.02, 0.02],
        "parking_rent_growth": [0, 0.02, 0.02, 0.02, 0.02],
        "occupancy_rate": 0.9,
        "operating_cost_per_sqm": 3000,
        "cost_growth_rates": [0, 0.02, 0.02, 0.02, 0.02],
        "replacement_reserve_rate": 0.03,
        "discount_rate": 0.12,
        "terminal_cap_rate": 0.10,
        "broker_commission": 0.01
    }
}

# Опции для выпадающих списков
PARAMETER_OPTIONS = {
    "hotel": {
        "hotel_category": ["4 звезды", "3 звезды"],
        "occupancy_rate": [0.50, 0.55, 0.60, 0.65, 0.70],
        "f_b_percentage": [0.20, 0.25, 0.30, 0.35],
        "other_revenue_percentage": [0.05, 0.10, 0.15, 0.20],
        "discount_rate": [0.10, 0.11, 0.12, 0.13, 0.14, 0.15],
        "terminal_cap_rate": [0.08, 0.09, 0.10, 0.11, 0.12]
    },
    "shopping_center": {
        "occupancy_rates": [
            [0.95, 0.95, 0.95, 0.95, 0.95],
            [0.98, 0.98, 0.98, 0.98, 0.98],
            [1.0, 1.0, 1.0, 1.0, 1.0]
        ],
        "operating_cost_per_sqm": [3000, 3500, 4000, 4500, 5000],
        "discount_rate": [0.10, 0.11, 0.12, 0.13, 0.14],
        "terminal_cap_rate": [0.08, 0.09, 0.10, 0.11, 0.12]
    },
    "office_center": {
        "class_type": ["A", "B", "C"],
        "occupancy_rate": [0.85, 0.90, 0.95, 1.0],
        "operating_cost_per_sqm": [2500, 3000, 3500, 4000],
        "discount_rate": [0.11, 0.12, 0.13, 0.14, 0.15],
        "terminal_cap_rate": [0.09, 0.10, 0.11, 0.12, 0.13]
    }
}


@router.post("/check", response_model=ParameterOptionsResponse)
async def check_parameters(request: ParameterCheckRequest):
    """
    Проверка недостающих параметров и возврат опций для выбора
    """
    try:
        property_type = request.property_type
        method = request.method
        property_data = request.property_data
        
        if property_type not in REQUIRED_PARAMETERS:
            raise HTTPException(
                status_code=400, 
                detail=f"Неподдерживаемый тип недвижимости: {property_type}"
            )
        
        if method not in REQUIRED_PARAMETERS[property_type]:
            raise HTTPException(
                status_code=400, 
                detail=f"Неподдерживаемый метод расчета: {method}"
            )
        
        required = REQUIRED_PARAMETERS[property_type][method]
        missing = []
        suggested = {}
        
        # Проверяем наличие параметров
        for param in required:
            if param not in property_data or property_data[param] is None or property_data[param] == "":
                missing.append(param)
                # Предлагаем значение по умолчанию если есть
                if property_type in DEFAULT_VALUES and param in DEFAULT_VALUES[property_type]:
                    suggested[param] = DEFAULT_VALUES[property_type][param]
        
        # Получаем опции для выпадающих списков
        options = {}
        if property_type in PARAMETER_OPTIONS:
            for param in missing:
                if param in PARAMETER_OPTIONS[property_type]:
                    options[param] = PARAMETER_OPTIONS[property_type][param]
        
        return ParameterOptionsResponse(
            missing_parameters=missing,
            parameter_options=options,
            suggested_values=suggested
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

