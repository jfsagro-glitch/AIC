import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Tabs, Tab, Paper } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CalculateIcon from '@mui/icons-material/Calculate';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getTabValue = () => {
    // Убираем basename из пути для сравнения
    const path = location.pathname.replace(/^\/AIC/, '') || '/';
    if (path === '/' || path === '') return 0;
    if (path === '/upload') return 1;
    if (path === '/calculate') return 2;
    if (path === '/history') return 3;
    if (path === '/settings') return 4;
    return 0;
  };

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    const routes = ['/', '/upload', '/calculate', '/history', '/settings'];
    navigate(routes[newValue]);
  };

  return (
    <Paper sx={{ mb: 2 }}>
      <Tabs
        value={getTabValue()}
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
