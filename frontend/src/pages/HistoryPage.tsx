import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Alert,
  CircularProgress,
  MenuItem,
  TextField,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import api from '../utils/api';

interface HistoryRecord {
  id: number;
  property_type: string;
  property_data: any;
  calculation_method: string;
  result: any;
  created_at: string;
}

const HistoryPage: React.FC = () => {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<string>('');

  useEffect(() => {
    loadHistory();
  }, [filterType]);

  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = filterType ? { property_type: filterType } : {};
      const response = await api.get('/api/history/', { params });
      setRecords(response.data.records);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при загрузке истории');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      return;
    }

    try {
      await api.delete(`/api/history/${id}`);
      loadHistory();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при удалении');
    }
  };

  const handleView = (record: HistoryRecord) => {
    const details = {
      property_type: record.property_type,
      calculation_method: record.calculation_method,
      property_value: record.result.property_value,
      ...record.result,
    };
    alert(JSON.stringify(details, null, 2));
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        История расчетов
      </Typography>

      <Box sx={{ mb: 2, display: 'flex', gap: 2 }}>
        <TextField
          select
          label="Фильтр по типу"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          sx={{ minWidth: 200 }}
        >
          <MenuItem value="">Все типы</MenuItem>
          <MenuItem value="hotel">Гостиницы</MenuItem>
          <MenuItem value="shopping_center">Торговые центры</MenuItem>
          <MenuItem value="office_center">Офисные центры</MenuItem>
        </TextField>
        <Button variant="outlined" onClick={loadHistory}>
          Обновить
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Тип объекта</TableCell>
                <TableCell>Метод расчета</TableCell>
                <TableCell>Стоимость</TableCell>
                <TableCell>Дата расчета</TableCell>
                <TableCell align="right">Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {records.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <Typography variant="body2" color="text.secondary">
                      История пуста
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                records.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>{record.id}</TableCell>
                    <TableCell>{record.property_type}</TableCell>
                    <TableCell>{record.calculation_method}</TableCell>
                    <TableCell>
                      {record.result.property_value?.toLocaleString('ru-RU', {
                        style: 'currency',
                        currency: 'RUB',
                        minimumFractionDigits: 0,
                      })}
                    </TableCell>
                    <TableCell>
                      {new Date(record.created_at).toLocaleString('ru-RU')}
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={() => handleView(record)}
                        color="primary"
                      >
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDelete(record.id)}
                        color="error"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default HistoryPage;
