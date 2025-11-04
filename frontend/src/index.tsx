import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Определяем basename для GitHub Pages
const getBasename = () => {
  // Если деплой на GitHub Pages, используем /AIC
  if (window.location.hostname === 'jfsagro-glitch.github.io' || 
      window.location.hostname.includes('github.io')) {
    return '/AIC';
  }
  // Для разработки и других деплоев basename не нужен
  return '';
};

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter basename={getBasename()}>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
