import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import DataUploadPage from './pages/DataUploadPage';
import CalculationPage from './pages/CalculationPage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI Залоговик
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Navigation />
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<DataUploadPage />} />
          <Route path="/calculate" element={<CalculationPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={
            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Typography variant="h4" gutterBottom>
                404 - Страница не найдена
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Запрашиваемая страница не существует.
              </Typography>
            </Box>
          } />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;
