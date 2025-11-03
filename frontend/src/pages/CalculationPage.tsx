import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  MenuItem,
  Grid,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import api from '../utils/api';
import AIAssistant from '../components/AIAssistant';

interface CalculationResult {
  success: boolean;
  result: {
    property_type: string;
    property_value: number;
    calculation_method: string;
    capitalization_result?: any;
    dcf_result?: any;
  };
}

const CalculationPage: React.FC = () => {
  const [propertyType, setPropertyType] = useState('hotel');
  const [method, setMethod] = useState('direct_capitalization');
  const [propertyData, setPropertyData] = useState<any>({});
  const [calculating, setCalculating] = useState(false);
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  const handlePropertyDataChange = (field: string, value: any) => {
    setPropertyData({
      ...propertyData,
      [field]: value,
      property_type: propertyType,
      assessment_date: new Date().toISOString(),
      // Устанавливаем значения по умолчанию
      occupancy_rate: propertyData.occupancy_rate || (propertyType === 'hotel' ? 0.55 : propertyType === 'shopping_center' ? 0.98 : 0.90),
      replacement_reserve_rate: propertyData.replacement_reserve_rate || 0.05,
      cap_rate: propertyData.cap_rate || 0.1,
    });
  };

  const handleCalculate = async () => {
    setCalculating(true);
    setError(null);

    try {
      const response = await api.post<CalculationResult>(
        `/api/valuation/calculate?method=${method}`,
        propertyData
      );
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при расчете');
    } finally {
      setCalculating(false);
    }
  };

  const renderPropertyForm = () => {
    if (propertyType === 'hotel') {
      return (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Количество номеров"
              type="number"
              value={propertyData.rooms_count || ''}
              onChange={(e) =>
                handlePropertyDataChange('rooms_count', parseInt(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              select
              label="Категория отеля"
              value={propertyData.hotel_category || ''}
              onChange={(e) =>
                handlePropertyDataChange('hotel_category', e.target.value)
              }
            >
              <MenuItem value="4 звезды">4 звезды</MenuItem>
              <MenuItem value="3 звезды">3 звезды</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="ADR (средняя цена за номер)"
              type="number"
              value={propertyData.adr || ''}
              onChange={(e) =>
                handlePropertyDataChange('adr', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Загрузка (коэффициент)"
              type="number"
              inputProps={{ step: 0.01, min: 0, max: 1 }}
              value={propertyData.occupancy_rate || ''}
              onChange={(e) =>
                handlePropertyDataChange('occupancy_rate', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Общая площадь (кв.м)"
              type="number"
              value={propertyData.total_area || ''}
              onChange={(e) =>
                handlePropertyDataChange('total_area', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Площадь участка (кв.м)"
              type="number"
              value={propertyData.land_area || ''}
              onChange={(e) =>
                handlePropertyDataChange('land_area', parseFloat(e.target.value))
              }
            />
          </Grid>
        </Grid>
      );
    } else if (propertyType === 'shopping_center') {
      return (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Арендная площадь (кв.м)"
              type="number"
              value={propertyData.current_lease_area || ''}
              onChange={(e) =>
                handlePropertyDataChange('current_lease_area', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Доход от базовой аренды"
              type="number"
              value={propertyData.base_rent_income || ''}
              onChange={(e) =>
                handlePropertyDataChange('base_rent_income', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Операционные сборы"
              type="number"
              value={propertyData.operation_rate_income || ''}
              onChange={(e) =>
                handlePropertyDataChange('operation_rate_income', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Маркетинговые сборы"
              type="number"
              value={propertyData.marketing_fee_income || ''}
              onChange={(e) =>
                handlePropertyDataChange('marketing_fee_income', parseFloat(e.target.value))
              }
            />
          </Grid>
        </Grid>
      );
    } else if (propertyType === 'office_center') {
      return (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              select
              label="Класс офисного центра"
              value={propertyData.class_type || ''}
              onChange={(e) =>
                handlePropertyDataChange('class_type', e.target.value)
              }
            >
              <MenuItem value="A">Класс A</MenuItem>
              <MenuItem value="B">Класс B</MenuItem>
              <MenuItem value="C">Класс C</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Ставка аренды за кв.м"
              type="number"
              value={propertyData.rent_rate_per_sqm || ''}
              onChange={(e) =>
                handlePropertyDataChange('rent_rate_per_sqm', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Общая площадь (кв.м)"
              type="number"
              value={propertyData.total_area || ''}
              onChange={(e) =>
                handlePropertyDataChange('total_area', parseFloat(e.target.value))
              }
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Загрузка (коэффициент)"
              type="number"
              inputProps={{ step: 0.01, min: 0, max: 1 }}
              value={propertyData.occupancy_rate || ''}
              onChange={(e) =>
                handlePropertyDataChange('occupancy_rate', parseFloat(e.target.value))
              }
            />
          </Grid>
        </Grid>
      );
    }
    return null;
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Расчет стоимости
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              select
              label="Тип недвижимости"
              value={propertyType}
              onChange={(e) => {
                setPropertyType(e.target.value);
                setPropertyData({});
              }}
            >
              <MenuItem value="hotel">Гостиница</MenuItem>
              <MenuItem value="shopping_center">Торговый центр</MenuItem>
              <MenuItem value="office_center">Офисный центр</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              select
              label="Метод расчета"
              value={method}
              onChange={(e) => setMethod(e.target.value)}
            >
              <MenuItem value="direct_capitalization">Прямая капитализация</MenuItem>
              <MenuItem value="dcf">ДДП (5 лет)</MenuItem>
            </TextField>
          </Grid>
        </Grid>

        <Box sx={{ mt: 3 }}>{renderPropertyForm()}</Box>

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleCalculate}
            disabled={calculating}
            fullWidth
          >
            {calculating ? <CircularProgress size={24} /> : 'Рассчитать'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="success">
              Расчет выполнен успешно!
            </Alert>
            <Typography variant="h5" sx={{ mt: 2 }}>
              Стоимость объекта: {result.result.property_value.toLocaleString('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 0,
              })}
            </Typography>

            <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ mt: 2 }}>
              <Tab label="Детали расчета" />
              <Tab label="AI Ассистент" />
            </Tabs>

            {tabValue === 0 && result.result.capitalization_result && (
              <TableContainer component={Paper} sx={{ mt: 2 }}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Показатель</TableCell>
                      <TableCell align="right">Значение</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>Валовой доход</TableCell>
                      <TableCell align="right">
                        {result.result.capitalization_result.gross_income.toLocaleString('ru-RU')}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Операционные расходы</TableCell>
                      <TableCell align="right">
                        {result.result.capitalization_result.operating_expenses.toLocaleString('ru-RU')}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Резерв на замещение</TableCell>
                      <TableCell align="right">
                        {result.result.capitalization_result.replacement_reserve.toLocaleString('ru-RU')}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Чистый операционный доход (NOI)</TableCell>
                      <TableCell align="right">
                        {result.result.capitalization_result.net_operating_income.toLocaleString('ru-RU')}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Ставка капитализации</TableCell>
                      <TableCell align="right">
                        {(result.result.capitalization_result.cap_rate * 100).toFixed(2)}%
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            )}

            {tabValue === 0 && result.result.dcf_result && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Дисконтированные денежные потоки (5 лет)
                </Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Год</TableCell>
                        <TableCell align="right">Валовой доход</TableCell>
                        <TableCell align="right">Операционные расходы</TableCell>
                        <TableCell align="right">NOI</TableCell>
                        <TableCell align="right">Коэффициент дисконтирования</TableCell>
                        <TableCell align="right">Текущая стоимость</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {result.result.dcf_result.yearly_cash_flows.map((flow: any) => (
                        <TableRow key={flow.year}>
                          <TableCell>{flow.year}</TableCell>
                          <TableCell align="right">
                            {flow.gross_income.toLocaleString('ru-RU')}
                          </TableCell>
                          <TableCell align="right">
                            {flow.operating_expenses.toLocaleString('ru-RU')}
                          </TableCell>
                          <TableCell align="right">
                            {flow.net_operating_income.toLocaleString('ru-RU')}
                          </TableCell>
                          <TableCell align="right">
                            {flow.discount_factor.toFixed(4)}
                          </TableCell>
                          <TableCell align="right">
                            {flow.present_value.toLocaleString('ru-RU')}
                          </TableCell>
                        </TableRow>
                      ))}
                      <TableRow>
                        <TableCell colSpan={5} align="right"><strong>Терминальная стоимость</strong></TableCell>
                        <TableCell align="right">
                          <strong>{result.result.dcf_result.terminal_value.toLocaleString('ru-RU')}</strong>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell colSpan={5} align="right"><strong>Итого текущая стоимость</strong></TableCell>
                        <TableCell align="right">
                          <strong>{result.result.dcf_result.present_value.toLocaleString('ru-RU')}</strong>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Ставка дисконтирования: {(result.result.dcf_result.discount_rate * 100).toFixed(2)}%
                </Typography>
              </Box>
            )}

            {tabValue === 1 && (
              <Box sx={{ mt: 2 }}>
                <AIAssistant propertyData={propertyData} result={result.result} />
              </Box>
            )}
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default CalculationPage;
