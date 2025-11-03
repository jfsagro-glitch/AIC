"""
Модули расчета стоимости недвижимости
"""
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel

# Локальные модели для расчетов
class CommercialProperty:
    def __init__(self, property_type, assessment_date, total_area, land_area, 
                 occupancy_rate, cap_rate, replacement_reserve_rate=0.05):
        self.property_type = property_type
        self.assessment_date = assessment_date
        self.total_area = total_area
        self.land_area = land_area
        self.occupancy_rate = occupancy_rate
        self.cap_rate = cap_rate
        self.replacement_reserve_rate = replacement_reserve_rate

class Hotel(CommercialProperty):
    def __init__(self, rooms_count, hotel_category, adr, **kwargs):
        super().__init__(**kwargs)
        self.rooms_count = rooms_count
        self.hotel_category = hotel_category
        self.adr = adr

class ShoppingCenter(CommercialProperty):
    def __init__(self, current_lease_area, base_rent_income, 
                 operation_rate_income, marketing_fee_income, **kwargs):
        super().__init__(**kwargs)
        self.current_lease_area = current_lease_area
        self.base_rent_income = base_rent_income
        self.operation_rate_income = operation_rate_income
        self.marketing_fee_income = marketing_fee_income

class OfficeCenter(CommercialProperty):
    def __init__(self, class_type, condition, rent_rate_per_sqm, **kwargs):
        super().__init__(**kwargs)
        self.class_type = class_type
        self.condition = condition
        self.rent_rate_per_sqm = rent_rate_per_sqm

class CapitalizationResult(BaseModel):
    gross_income: float
    operating_expenses: float
    replacement_reserve: float
    net_operating_income: float
    cap_rate: float
    property_value: float
    method: str = "direct_capitalization"

class DCFResult(BaseModel):
    yearly_cash_flows: list[dict]
    terminal_value: float
    present_value: float
    total_value: float
    method: str = "dcf"
    discount_rate: float

def get_cap_rate(property: CommercialProperty) -> float:
    """Получить ставку капитализации для объекта"""
    if isinstance(property, Hotel):
        if property.hotel_category == "4 звезды":
            return 0.1075
        elif property.hotel_category == "3 звезды":
            return 0.1125
    elif isinstance(property, ShoppingCenter):
        return 0.105
    elif isinstance(property, OfficeCenter):
        if property.class_type == "A":
            return 0.135
        elif property.class_type == "B":
            return 0.14
        elif property.class_type == "C":
            return 0.145
    
    return property.cap_rate

def calculate_gross_income(property: CommercialProperty) -> float:
    """Расчет валового дохода"""
    if isinstance(property, Hotel):
        # Для отеля: количество комнат * ADR * загрузка * 365 дней
        return property.rooms_count * property.adr * property.occupancy_rate * 365
    
    elif isinstance(property, ShoppingCenter):
        # Для ТЦ: доход от аренды + операционные сборы + маркетинговые сборы
        return (
            property.base_rent_income +
            property.operation_rate_income +
            property.marketing_fee_income
        )
    
    elif isinstance(property, OfficeCenter):
        # Для офисного центра: площадь * ставка аренды за кв.м в месяц * 12 месяцев * загрузка
        # Если rent_rate_per_sqm - месячная ставка, умножаем на 12
        monthly_rent = property.total_area * property.rent_rate_per_sqm * property.occupancy_rate
        return monthly_rent * 12  # Годовая арендная плата
    
    return 0.0

def calculate_operating_expenses(property: CommercialProperty, gross_income: float) -> float:
    """Расчет операционных расходов"""
    # Операционные расходы как процент от валового дохода
    expense_rates = {
        "hotel": 0.35,  # 35% для отелей
        "shopping_center": 0.25,  # 25% для ТЦ
        "office_center": 0.30  # 30% для офисных центров
    }
    
    expense_rate = expense_rates.get(property.property_type, 0.30)
    return gross_income * expense_rate

def direct_capitalization(property: CommercialProperty) -> CapitalizationResult:
    """
    Расчет методом прямой капитализации для всех типов недвижимости
    """
    # 1. Расчет валового дохода
    gross_income = calculate_gross_income(property)
    
    # 2. Вычет операционных расходов
    operating_expenses = calculate_operating_expenses(property, gross_income)
    
    # 3. Вычет резерва на замещение
    replacement_reserve = gross_income * property.replacement_reserve_rate
    
    # 4. Расчет чистого операционного дохода (NOI)
    net_operating_income = gross_income - operating_expenses - replacement_reserve
    
    # 5. Получение ставки капитализации
    cap_rate = get_cap_rate(property)
    
    # 6. Применение ставки капитализации
    property_value = net_operating_income / cap_rate if cap_rate > 0 else 0
    
    return CapitalizationResult(
        gross_income=gross_income,
        operating_expenses=operating_expenses,
        replacement_reserve=replacement_reserve,
        net_operating_income=net_operating_income,
        cap_rate=cap_rate,
        property_value=property_value,
        method="direct_capitalization"
    )

def dcf_valuation(property: CommercialProperty, years: int = 5, discount_rate: float = 0.12) -> DCFResult:
    """
    Расчет методом ДДП с прогнозом на 5 лет
    """
    yearly_cash_flows = []
    present_value_total = 0.0
    
    # Базовые показатели первого года
    base_gross_income = calculate_gross_income(property)
    base_operating_expenses = calculate_operating_expenses(property, base_gross_income)
    base_replacement_reserve = base_gross_income * property.replacement_reserve_rate
    base_noi = base_gross_income - base_operating_expenses - base_replacement_reserve
    
    # Прогноз роста (консервативный - 2% в год)
    growth_rate = 0.02
    
    # Прогноз денежных потоков на каждый год
    for year in range(1, years + 1):
        # Применение роста
        growth_factor = (1 + growth_rate) ** (year - 1)
        
        gross_income = base_gross_income * growth_factor
        operating_expenses = base_operating_expenses * growth_factor
        replacement_reserve = base_replacement_reserve * growth_factor
        noi = gross_income - operating_expenses - replacement_reserve
        
        # Дисконтирование
        discount_factor = 1 / ((1 + discount_rate) ** year)
        present_value = noi * discount_factor
        present_value_total += present_value
        
        yearly_cash_flows.append({
            "year": year,
            "gross_income": round(gross_income, 2),
            "operating_expenses": round(operating_expenses, 2),
            "replacement_reserve": round(replacement_reserve, 2),
            "net_operating_income": round(noi, 2),
            "discount_factor": round(discount_factor, 4),
            "present_value": round(present_value, 2)
        })
    
    # Расчет терминальной стоимости (NOI последнего года / cap_rate)
    cap_rate = get_cap_rate(property)
    terminal_noi = yearly_cash_flows[-1]["net_operating_income"]
    terminal_value_nominal = terminal_noi / cap_rate if cap_rate > 0 else 0
    terminal_value_pv = terminal_value_nominal / ((1 + discount_rate) ** years)
    
    total_value = present_value_total + terminal_value_pv
    
    return DCFResult(
        yearly_cash_flows=yearly_cash_flows,
        terminal_value=round(terminal_value_pv, 2),
        present_value=round(present_value_total, 2),
        total_value=round(total_value, 2),
        method="dcf",
        discount_rate=discount_rate
    )
