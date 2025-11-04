import React, { useMemo } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Tabs, Tab, Paper } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CalculateIcon from '@mui/icons-material/Calculate';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';

const ROUTES = ['/', '/upload', '/calculate', '/history', '/settings'] as const;

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const tabValue = useMemo(() => {
    // Убираем basename из пути для сравнения
    const path = location.pathname.replace(/^\/AIC/, '') || '/';
    if (path === '/' || path === '') return 0;
    if (path === '/upload') return 1;
    if (path === '/calculate') return 2;
    if (path === '/history') return 3;
    if (path === '/settings') return 4;
    return 0;
  }, [location.pathname]);

  const handleChange = React.useCallback((_event: React.SyntheticEvent, newValue: number) => {
    navigate(ROUTES[newValue]);
  }, [navigate]);

  return (
    <Paper sx={{ mb: 2 }}>
      <Tabs
        value={tabValue}
        onChange={handleChange}
        variant="fullWidth"
        indicatorColor="primary"
        textColor="primary"
      >
        <Tab icon={<HomeIcon />} label="Главная" />
        <Tab icon={<UploadFileIcon />} label="Загрузка данных" />
        <Tab icon={<CalculateIcon />} label="Расчет" />
        <Tab icon={<HistoryIcon />} label="История" />
        <Tab icon={<SettingsIcon />} label="Настройки" />
      </Tabs>
    </Paper>
  );
};

export default Navigation;
