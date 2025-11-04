"""
Детальный калькулятор ДДП (дисконтированных денежных потоков)
для оценки коммерческой недвижимости
"""
from typing import Dict, List, Any, Tuple
from datetime import datetime


class DCFCalculator:
    """Универсальный калькулятор ДДП для всех типов недвижимости"""
    
    def __init__(self, property_data: Dict[str, Any], forecast_years: int = 5):
        self.property_data = property_data
        self.forecast_years = forecast_years
        self.days_in_year = 365
    
    # ========== ГОСТИНИЦЫ ==========
    
    def calculate_hotel_revenues(self) -> List[Dict[str, Any]]:
        """Расчет доходов гостиницы"""
        revenues = []
        
        rooms_count = self.property_data.get('rooms_count', 0)
        occupancy_rate = self.property_data.get('occupancy_rate', 0.55)
        adr = self.property_data.get('adr', 0)
        
        # Рост ставок аренды по годам (по умолчанию)
        rent_growth_rate = self.property_data.get(
            'rent_growth_rate', 
            [0.03, 0.02, 0.05, 0.02, 0.02]
        )
        
        # Проценты для F&B и прочей выручки
        f_b_percentage = self.property_data.get('f_b_percentage', 0.25)
        other_revenue_percentage = self.property_data.get('other_revenue_percentage', 0.10)
        
        current_adr = adr
        
        for year in range(self.forecast_years):
            # Расчет ADR с учетом роста
            growth = rent_growth_rate[year] if year < len(rent_growth_rate) else 0.02
            current_adr = current_adr * (1 + growth)
            
            # Расчет RevPAR
            revpar = current_adr * occupancy_rate
            
            # Доход от номерного фонда
            room_revenue = (
                self.days_in_year * rooms_count * 
                occupancy_rate * current_adr
            )
            
            # F&B доход
            f_b_revenue = room_revenue * f_b_percentage
            
            # Прочая выручка
            other_revenue = room_revenue * other_revenue_percentage
            
            # Итого выручка
            total_revenue = room_revenue + f_b_revenue + other_revenue
            
            revenues.append({
                'year': year + 1,
                'adr': round(current_adr, 2),
                'revpar': round(revpar, 2),
                'room_revenue': round(room_revenue, 2),
                'f_b_revenue': round(f_b_revenue, 2),
                'other_revenue': round(other_revenue, 2),
                'total_revenue': round(total_revenue, 2)
            })
        
        return revenues
    
    def calculate_hotel_expenses(self, revenues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Расчет расходов гостиницы"""
        expenses = []
        
        # Проценты расходов
        room_maintenance_percentage = self.property_data.get('room_maintenance_percentage', 0.15)
        f_b_expense_percentage = self.property_data.get('f_b_expense_percentage', 0.35)
        other_expense_percentage = self.property_data.get('other_expense_percentage', 0.20)
        
        # Нераспределяемые расходы
        admin_expense_percentage = self.property_data.get('admin_expense_percentage', 0.05)
        marketing_expense_percentage = self.property_data.get('marketing_expense_percentage', 0.03)
        maintenance_expense_percentage = self.property_data.get('maintenance_expense_percentage', 0.04)
        utilities_expense_percentage = self.property_data.get('utilities_expense_percentage', 0.06)
        
        # Вознаграждение оператора
        base_management_fee_percentage = self.property_data.get('base_management_fee_percentage', 0.03)
        incentive_fee_percentage = self.property_data.get('incentive_fee_percentage', 0.10)
        royalty_percentage = self.property_data.get('royalty_percentage', 0.04)
        
        # Фиксированные расходы
        property_tax = self.property_data.get('property_tax', 0)
        land_payments = self.property_data.get('land_payments', 0)
        insurance = self.property_data.get('insurance', 0)
        
        # Резерв на замещение
        replacement_reserve_rate = self.property_data.get('replacement_reserve_rate', 0.03)
        
        for revenue in revenues:
            # Прямые расходы
            room_maintenance_expense = revenue['room_revenue'] * room_maintenance_percentage
            f_b_expense = revenue['f_b_revenue'] * f_b_expense_percentage
            other_expense = revenue['other_revenue'] * other_expense_percentage
            total_direct_expenses = room_maintenance_expense + f_b_expense + other_expense
            
            # Нераспределяемые расходы
            admin_expense = revenue['total_revenue'] * admin_expense_percentage
            marketing_expense = revenue['total_revenue'] * marketing_expense_percentage
            maintenance_expense = revenue['total_revenue'] * maintenance_expense_percentage
            utilities_expense = revenue['total_revenue'] * utilities_expense_percentage
            total_undistributed_expenses = (
                admin_expense + marketing_expense + 
                maintenance_expense + utilities_expense
            )
            
            # Вознаграждение оператора
            base_management_fee = revenue['total_revenue'] * base_management_fee_percentage
            
            # Расчет GOP для incentive fee
            gop = revenue['total_revenue'] - total_direct_expenses - total_undistributed_expenses
            incentive_fee = max(0, gop * incentive_fee_percentage)
            
            royalty_fee = revenue['room_revenue'] * royalty_percentage
            total_operator_fees = base_management_fee + incentive_fee + royalty_fee
            
            # Фиксированные расходы
            total_fixed_expenses = property_tax + land_payments + insurance
            
            # Резерв на замещение
            replacement_reserve = revenue['total_revenue'] * replacement_reserve_rate
            
            # Итого операционные расходы
            total_operating_expenses = (
                total_direct_expenses + total_undistributed_expenses + 
                total_operator_fees + total_fixed_expenses + replacement_reserve
            )
            
            expenses.append({
                'room_maintenance_expense': round(room_maintenance_expense, 2),
                'f_b_expense': round(f_b_expense, 2),
                'other_expense': round(other_expense, 2),
                'total_direct_expenses': round(total_direct_expenses, 2),
                'admin_expense': round(admin_expense, 2),
                'marketing_expense': round(marketing_expense, 2),
                'maintenance_expense': round(maintenance_expense, 2),
                'utilities_expense': round(utilities_expense, 2),
                'total_undistributed_expenses': round(total_undistributed_expenses, 2),
                'base_management_fee': round(base_management_fee, 2),
                'incentive_fee': round(incentive_fee, 2),
                'royalty_fee': round(royalty_fee, 2),
                'total_operator_fees': round(total_operator_fees, 2),
                'total_fixed_expenses': round(total_fixed_expenses, 2),
                'replacement_reserve': round(replacement_reserve, 2),
                'total_operating_expenses': round(total_operating_expenses, 2)
            })
        
        return expenses
    
    def calculate_hotel_noi(self, revenues: List[Dict], expenses: List[Dict]) -> List[float]:
        """Расчет чистого операционного дохода для гостиницы"""
        noi_list = []
        for i in range(len(revenues)):
            noi = revenues[i]['total_revenue'] - expenses[i]['total_operating_expenses']
            noi_list.append(round(noi, 2))
        return noi_list
    
    # ========== ТОРГОВЫЕ ЦЕНТРЫ ==========
    
    def calculate_shopping_center_revenues(self) -> List[Dict[str, Any]]:
        """Расчет доходов торгового центра"""
        revenues = []
        
        total_area = self.property_data.get('total_area', 0)
        lease_area = self.property_data.get('current_lease_area', 0)
        base_rent_rate = self.property_data.get('base_rent_rate', 0)
        
        # Рост ставок и загрузка по годам
        rent_growth_rates = self.property_data.get(
            'rent_growth_rates', 
            [0, 0.02, 0.02, 0.02, 0.02]
        )
        occupancy_rates = self.property_data.get(
            'occupancy_rates', 
            [0.98, 0.98, 0.98, 0.98, 0.98]
        )
        
        current_rent_rate = base_rent_rate
        
        for year in range(self.forecast_years):
            # Увеличение ставки аренды
            growth = rent_growth_rates[year] if year < len(rent_growth_rates) else 0.02
            current_rent_rate = current_rent_rate * (1 + growth)
            
            # Действительный валовый доход
            occupancy = occupancy_rates[year] if year < len(occupancy_rates) else 0.98
            dvd = (lease_area * current_rent_rate) * occupancy
            
            revenues.append({
                'year': year + 1,
                'rent_rate': round(current_rent_rate, 2),
                'occupancy_rate': occupancy,
                'dvd': round(dvd, 2)
            })
        
        return revenues
    
    def calculate_shopping_center_expenses(self, revenues: List[Dict]) -> List[Dict[str, Any]]:
        """Расчет расходов торгового центра"""
        expenses = []
        
        total_area = self.property_data.get('total_area', 0)
        operating_cost_per_sqm = self.property_data.get('operating_cost_per_sqm', 3500)
        
        cost_growth_rates = self.property_data.get(
            'cost_growth_rates', 
            [0, 0.02, 0.02, 0.02, 0.02]
        )
        replacement_reserve_rate = self.property_data.get('replacement_reserve_rate', 0.03)
        
        current_operating_cost = operating_cost_per_sqm
        
        for i, revenue in enumerate(revenues):
            # Увеличение расходов
            growth = cost_growth_rates[i] if i < len(cost_growth_rates) else 0.02
            current_operating_cost = current_operating_cost * (1 + growth)
            
            # Итого операционные расходы
            operating_expenses = current_operating_cost * total_area
            
            # Капитальный резерв
            replacement_reserve = revenue['dvd'] * replacement_reserve_rate
            
            # Итого расходы
            total_expenses = operating_expenses + replacement_reserve
            
            expenses.append({
                'operating_cost_per_sqm': round(current_operating_cost, 2),
                'operating_expenses': round(operating_expenses, 2),
                'replacement_reserve': round(replacement_reserve, 2),
                'total_expenses': round(total_expenses, 2)
            })
        
        return expenses
    
    # ========== ОФИСНЫЕ ЦЕНТРЫ ==========
    
    def calculate_office_center_revenues(self) -> List[Dict[str, Any]]:
        """Расчет доходов офисного центра"""
        revenues = []
        
        total_area = self.property_data.get('total_area', 0)
        lease_area = self.property_data.get('lease_area', 0)
        parking_spaces = self.property_data.get('parking_spaces', 0)
        
        office_rent_rate = self.property_data.get('office_rent_rate', 0)
        parking_rate = self.property_data.get('parking_rate', 0)
        
        office_rent_growth = self.property_data.get(
            'office_rent_growth', 
            [0, 0.02, 0.02, 0.02, 0.02]
        )
        parking_rent_growth = self.property_data.get(
            'parking_rent_growth', 
            [0, 0.02, 0.02, 0.02, 0.02]
        )
        occupancy_rate = self.property_data.get('occupancy_rate', 0.9)
        
        current_office_rate = office_rent_rate
        current_parking_rate = parking_rate
        
        for year in range(self.forecast_years):
            # Увеличение ставок
            office_growth = office_rent_growth[year] if year < len(office_rent_growth) else 0.02
            parking_growth = parking_rent_growth[year] if year < len(parking_rent_growth) else 0.02
            
            current_office_rate = current_office_rate * (1 + office_growth)
            current_parking_rate = current_parking_rate * (1 + parking_growth)
            
            # Доход от офисов
            office_income = (lease_area * current_office_rate) * occupancy_rate
            
            # Доход от парковки
            parking_income = (parking_spaces * current_parking_rate) * occupancy_rate
            
            # Общий доход
            total_income = office_income + parking_income
            
            revenues.append({
                'year': year + 1,
                'office_rent_rate': round(current_office_rate, 2),
                'parking_rent_rate': round(current_parking_rate, 2),
                'office_income': round(office_income, 2),
                'parking_income': round(parking_income, 2),
                'total_income': round(total_income, 2)
            })
        
        return revenues
    
    def calculate_office_center_expenses(self, revenues: List[Dict]) -> List[Dict[str, Any]]:
        """Расчет расходов офисного центра"""
        expenses = []
        
        total_area = self.property_data.get('total_area', 0)
        operating_cost_per_sqm = self.property_data.get('operating_cost_per_sqm', 3000)
        
        cost_growth_rates = self.property_data.get(
            'cost_growth_rates', 
            [0, 0.02, 0.02, 0.02, 0.02]
        )
        replacement_reserve_rate = self.property_data.get('replacement_reserve_rate', 0.03)
        
        current_operating_cost = operating_cost_per_sqm
        
        for i, revenue in enumerate(revenues):
            # Увеличение расходов
            growth = cost_growth_rates[i] if i < len(cost_growth_rates) else 0.02
            current_operating_cost = current_operating_cost * (1 + growth)
            
            # Операционные расходы
            operating_expenses = current_operating_cost * total_area
            
            # Резерв на замещение
            replacement_reserve = revenue['total_income'] * replacement_reserve_rate
            
            # Итого расходы
            total_expenses = operating_expenses + replacement_reserve
            
            expenses.append({
                'operating_cost_per_sqm': round(current_operating_cost, 2),
                'operating_expenses': round(operating_expenses, 2),
                'replacement_reserve': round(replacement_reserve, 2),
                'total_expenses': round(total_expenses, 2)
            })
        
        return expenses
    
    # ========== УНИВЕРСАЛЬНЫЕ ФУНКЦИИ ==========
    
    def calculate_discount_factors(self) -> Tuple[List[float], List[float]]:
        """Расчет коэффициентов дисконтирования"""
        discount_rate = self.property_data.get('discount_rate', 0.12)
        
        mid_year_factors = []
        end_year_factors = []
        
        for year in range(1, self.forecast_years + 1):
            # В середине года
            mid_year_factor = (1 / (1 + discount_rate)) ** (year - 0.5)
            mid_year_factors.append(round(mid_year_factor, 6))
            
            # В конце года
            end_year_factor = (1 / (1 + discount_rate)) ** year
            end_year_factors.append(round(end_year_factor, 6))
        
        return mid_year_factors, end_year_factors
    
    def calculate_terminal_value(self, final_year_noi: float) -> float:
        """Расчет терминальной стоимости"""
        terminal_cap_rate = self.property_data.get('terminal_cap_rate', 0.10)
        broker_commission = self.property_data.get('broker_commission', 0.01)
        
        # Стоимость реверсии
        terminal_value = final_year_noi / terminal_cap_rate
        
        # За вычетом комиссионных
        terminal_value_net = terminal_value * (1 - broker_commission)
        
        return round(terminal_value_net, 2)
    
    def calculate_market_value(
        self, 
        noi_list: List[float], 
        mid_factors: List[float], 
        end_factors: List[float]
    ) -> Dict[str, Any]:
        """Итоговый расчет рыночной стоимости"""
        # Текущая стоимость будущих доходов
        pv_cash_flows = sum(
            noi * factor 
            for noi, factor in zip(noi_list, mid_factors)
        )
        
        # Текущая стоимость реверсии
        terminal_value = self.calculate_terminal_value(noi_list[-1])
        pv_terminal = terminal_value * end_factors[-1]
        
        # Рыночная стоимость
        market_value = pv_cash_flows + pv_terminal
        
        total_area = self.property_data.get('total_area', 1)
        
        return {
            'market_value': round(market_value, 2),
            'pv_cash_flows': round(pv_cash_flows, 2),
            'pv_terminal': round(pv_terminal, 2),
            'terminal_value': terminal_value,
            'value_per_sqm': round(market_value / total_area, 2) if total_area > 0 else 0
        }
    
    # ========== ГЛАВНАЯ ФУНКЦИЯ ==========
    
    def calculate_dcf(self, property_type: str) -> Dict[str, Any]:
        """Универсальный расчет ДДП"""
        revenues = []
        expenses = []
        noi_list = []
        
        if property_type == 'hotel':
            revenues = self.calculate_hotel_revenues()
            expenses = self.calculate_hotel_expenses(revenues)
            noi_list = self.calculate_hotel_noi(revenues, expenses)
        
        elif property_type == 'shopping_center':
            revenues = self.calculate_shopping_center_revenues()
            expenses = self.calculate_shopping_center_expenses(revenues)
            noi_list = [
                rev['dvd'] - exp['total_expenses'] 
                for rev, exp in zip(revenues, expenses)
            ]
        
        elif property_type == 'office_center':
            revenues = self.calculate_office_center_revenues()
            expenses = self.calculate_office_center_expenses(revenues)
            noi_list = [
                rev['total_income'] - exp['total_expenses'] 
                for rev, exp in zip(revenues, expenses)
            ]
        else:
            raise ValueError(f"Неподдерживаемый тип недвижимости: {property_type}")
        
        # Расчет коэффициентов дисконтирования
        mid_factors, end_factors = self.calculate_discount_factors()
        
        # Расчет рыночной стоимости
        market_value_result = self.calculate_market_value(noi_list, mid_factors, end_factors)
        
        # Формирование детализированного результата
        yearly_cash_flows = []
        for i in range(self.forecast_years):
            yearly_cash_flows.append({
                'year': i + 1,
                'revenue': revenues[i],
                'expenses': expenses[i],
                'noi': noi_list[i],
                'discount_factor_mid': mid_factors[i],
                'discount_factor_end': end_factors[i],
                'present_value': round(noi_list[i] * mid_factors[i], 2)
            })
        
        return {
            'property_type': property_type,
            'forecast_years': self.forecast_years,
            'discount_rate': self.property_data.get('discount_rate', 0.12),
            'yearly_cash_flows': yearly_cash_flows,
            'noi_list': noi_list,
            'terminal_value': market_value_result['terminal_value'],
            'pv_cash_flows': market_value_result['pv_cash_flows'],
            'pv_terminal': market_value_result['pv_terminal'],
            'market_value': market_value_result['market_value'],
            'value_per_sqm': market_value_result['value_per_sqm'],
            'method': 'dcf'
        }

