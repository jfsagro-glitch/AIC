import axios from 'axios';

// Определяем базовый URL API
const getApiUrl = () => {
  // В production или Docker используем переменную окружения
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  // Если деплой на GitHub Pages, используем Render backend
  if (window.location.hostname === 'jfsagro-glitch.github.io' || 
      window.location.hostname.includes('github.io')) {
    return 'https://aic-backend.onrender.com';
  }
  // Для разработки используем localhost
  return 'http://localhost:8000';
};

export const API_URL = getApiUrl();

// Создаем экземпляр axios с базовой конфигурацией
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Сервер вернул ошибку
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Запрос был отправлен, но ответ не получен
      console.error('Network Error:', error.request);
    } else {
      // Ошибка при настройке запроса
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
