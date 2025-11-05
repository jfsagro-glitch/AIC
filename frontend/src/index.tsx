import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';
import ErrorBoundary from './components/ErrorBoundary';

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

// Определяем basename для GitHub Pages (вычисляем один раз при загрузке)
const BASENAME = (() => {
  // Если деплой на GitHub Pages, используем /AIC
  if (window.location.hostname === 'jfsagro-glitch.github.io' || 
      window.location.hostname.includes('github.io')) {
    return '/AIC';
  }
  // Для разработки и других деплоев basename не нужен
  return '';
})();

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter basename={BASENAME}>
          <App />
        </BrowserRouter>
      </ThemeProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
