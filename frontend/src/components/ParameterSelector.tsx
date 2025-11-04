import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Checkbox,
  FormControlLabel,
  Alert,
  CircularProgress,
} from '@mui/material';
import api from '../utils/api';

interface ParameterSelectorProps {
  propertyType: string;
  method: string;
  propertyData: any;
  onParametersSelected: (selectedParams: any) => void;
  onClose: () => void;
}

const ParameterSelector: React.FC<ParameterSelectorProps> = ({
  propertyType,
  method,
  propertyData,
  onParametersSelected,
  onClose,
}) => {
  const [missingParams, setMissingParams] = useState<string[]>([]);
  const [parameterOptions, setParameterOptions] = useState<any>({});
  const [suggestedValues, setSuggestedValues] = useState<any>({});
  const [selectedParams, setSelectedParams] = useState<any>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkParameters();
  }, []);

  const checkParameters = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/parameters/check', {
        property_type: propertyType,
        method,
        property_data: propertyData,
      });
      setMissingParams(response.data.missing_parameters);
      setParameterOptions(response.data.parameter_options);
      setSuggestedValues(response.data.suggested_values);
      
      // Автоматически заполняем предложенные значения
      setSelectedParams(response.data.suggested_values);
    } catch (error: any) {
      console.error('Error checking parameters:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleParamChange = (param: string, value: any) => {
    setSelectedParams((prev: any) => ({
      ...prev,
      [param]: value,
    }));
  };

  const handleApply = () => {
    onParametersSelected(selectedParams);
    onClose();
  };

  if (loading) {
    return (
      <Dialog open={true} maxWidth="md" fullWidth>
        <DialogContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        </DialogContent>
      </Dialog>
    );
  }

  if (missingParams.length === 0) {
    return null;
  }

  return (
    <Dialog open={true} maxWidth="md" fullWidth onClose={onClose}>
      <DialogTitle>
        Выберите недостающие параметры
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Необходимо указать {missingParams.length} параметр(ов) для расчета методом ДДП
        </Alert>

        <Grid container spacing={2}>
          {missingParams.map((param) => {
            const options = parameterOptions[param];
            const suggested = suggestedValues[param];
            
            return (
              <Grid item xs={12} md={6} key={param}>
                {options && Array.isArray(options) ? (
                  <TextField
                    fullWidth
                    select
                    label={getParamLabel(param)}
                    value={selectedParams[param] || ''}
                    onChange={(e) => handleParamChange(param, e.target.value)}
                  >
                    {options.map((option: any, index: number) => (
                      <MenuItem key={index} value={option}>
                        {Array.isArray(option) 
                          ? option.map((v: any, i: number) => `${v.toFixed(2)}`).join(', ')
                          : typeof option === 'number'
                          ? option.toFixed(2)
                          : String(option)
                        }
                      </MenuItem>
                    ))}
                  </TextField>
                ) : (
                  <TextField
                    fullWidth
                    label={getParamLabel(param)}
                    type="number"
                    value={selectedParams[param] || suggested || ''}
                    onChange={(e) => {
                      const value = e.target.value;
                      // Обработка массивов (для rent_growth_rate и т.д.)
                      if (param.includes('growth') || param.includes('rates')) {
                        // Если это массив, разбиваем по запятым
                        const values = value.split(',').map((v) => parseFloat(v.trim())).filter((v) => !isNaN(v));
                        handleParamChange(param, values.length > 0 ? values : [0, 0, 0, 0, 0]);
                      } else {
                        handleParamChange(param, parseFloat(value) || 0);
                      }
                    }}
                    helperText={suggested ? `Рекомендуется: ${Array.isArray(suggested) ? suggested.join(', ') : suggested}` : ''}
                  />
                )}
              </Grid>
            );
          })}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Отмена</Button>
        <Button variant="contained" onClick={handleApply}>
          Применить
        </Button>
      </DialogActions>
    </Dialog>
  );
};

function getParamLabel(param: string): string {
  const labels: { [key: string]: string } = {
    rooms_count: 'Количество номеров',
    occupancy_rate: 'Коэффициент загрузки',
    adr: 'ADR (средняя цена за номер)',
    rent_growth_rate: 'Рост ставок аренды (по годам через запятую)',
    f_b_percentage: 'F&B доход (% от продажи номеров)',
    other_revenue_percentage: 'Прочая выручка (% от продажи номеров)',
    room_maintenance_percentage: 'Расходы на обслуживание номеров (%)',
    f_b_expense_percentage: 'Расходы на F&B (%)',
    other_expense_percentage: 'Расходы прочей выручки (%)',
    admin_expense_percentage: 'Административные расходы (%)',
    marketing_expense_percentage: 'Маркетинговые расходы (%)',
    maintenance_expense_percentage: 'Расходы на содержание (%)',
    utilities_expense_percentage: 'Коммунальные расходы (%)',
    base_management_fee_percentage: 'Базовое вознаграждение оператора (%)',
    incentive_fee_percentage: 'Стимулирующее вознаграждение (%)',
    royalty_percentage: 'Роялти (%)',
    property_tax: 'Налог на имущество',
    land_payments: 'Платежи за землю',
    insurance: 'Страхование',
    replacement_reserve_rate: 'Резерв на замещение (%)',
    discount_rate: 'Ставка дисконтирования',
    terminal_cap_rate: 'Терминальная ставка капитализации',
    broker_commission: 'Комиссия брокера (%)',
    total_area: 'Общая площадь (кв.м)',
    current_lease_area: 'Арендованная площадь (кв.м)',
    base_rent_rate: 'Базовая ставка аренды (руб/кв.м)',
    rent_growth_rates: 'Рост ставок аренды (по годам через запятую)',
    occupancy_rates: 'Коэффициенты загрузки (по годам через запятую)',
    operating_cost_per_sqm: 'Операционные расходы (руб/кв.м)',
    cost_growth_rates: 'Рост расходов (по годам через запятую)',
    lease_area: 'Арендованная площадь (кв.м)',
    parking_spaces: 'Количество парковочных мест',
    office_rent_rate: 'Ставка аренды офисов (руб/кв.м)',
    parking_rate: 'Ставка аренды парковки (руб/место)',
    office_rent_growth: 'Рост ставок офисов (по годам через запятую)',
    parking_rent_growth: 'Рост ставок парковки (по годам через запятую)',
  };
  
  return labels[param] || param;
}

export default ParameterSelector;

