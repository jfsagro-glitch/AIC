from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel

# SQLAlchemy модели для БД
class ValuationRecord(Base):
    __tablename__ = "valuation_records"

    id = Column(Integer, primary_key=True, index=True)
    property_type = Column(String, nullable=False)
    property_data = Column(JSON, nullable=False)
    calculation_method = Column(String, nullable=False)  # "direct_capitalization" or "dcf"
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic модели для API
class CommercialProperty(PydanticBaseModel):
    property_type: str  # "hotel", "shopping_center", "office_center"
    assessment_date: datetime
    total_area: float
    land_area: float
    occupancy_rate: float
    cap_rate: float
    replacement_reserve_rate: float = 0.05

class Hotel(CommercialProperty):
    rooms_count: int
    hotel_category: str  # "4 звезды", "3 звезды"
    adr: float  # Average Daily Rate

class ShoppingCenter(CommercialProperty):
    current_lease_area: float
    base_rent_income: float
    operation_rate_income: float
    marketing_fee_income: float

class OfficeCenter(CommercialProperty):
    class_type: str  # "A", "B", "C"
    condition: str
    rent_rate_per_sqm: float

class CapitalizationResult(PydanticBaseModel):
    gross_income: float
    operating_expenses: float
    replacement_reserve: float
    net_operating_income: float
    cap_rate: float
    property_value: float
    method: str = "direct_capitalization"

class DCFResult(PydanticBaseModel):
    yearly_cash_flows: list[dict]
    terminal_value: float
    present_value: float
    total_value: float
    method: str = "dcf"
    discount_rate: float

class ValuationResult(PydanticBaseModel):
    property_type: str
    property_value: float
    calculation_method: str
    capitalization_result: Optional[CapitalizationResult] = None
    dcf_result: Optional[DCFResult] = None
    calculation_date: datetime

class ValidationResult(PydanticBaseModel):
    is_valid: bool
    needs_correction: bool
    recommendations: list[str]
    confidence_score: float
