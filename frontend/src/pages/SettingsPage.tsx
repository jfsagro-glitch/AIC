import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Alert,
  Divider,
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';

const SettingsPage: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Загружаем сохраненный API ключ из localStorage
    const savedKey = localStorage.getItem('deepseek_api_key');
    if (savedKey) {
      setApiKey(savedKey);
    }
  }, []);

  const handleSave = () => {
    // Сохраняем в localStorage (в реальном приложении это должно быть на backend)
    localStorage.setItem('deepseek_api_key', apiKey);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Настройки
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          API Ключи
        </Typography>
        <Divider sx={{ mb: 2 }} />

        <TextField
          fullWidth
          label="DeepSeek API Key"
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          helperText="Получите API ключ на platform.deepseek.com"
          sx={{ mb: 2 }}
        />

        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={handleSave}
        >
          Сохранить
        </Button>

        {saved && (
          <Alert severity="success" sx={{ mt: 2 }}>
            Настройки сохранены!
          </Alert>
        )}
      </Paper>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Информация о системе
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="body2" paragraph>
          <strong>Версия:</strong> 1.0.0
        </Typography>
        <Typography variant="body2" paragraph>
          <strong>Поддерживаемые типы объектов:</strong>
        </Typography>
        <ul>
          <li>Гостиницы (4 и 3 звезды)</li>
          <li>Торговые центры</li>
          <li>Офисные центры (классы A, B, C)</li>
        </ul>
        <Typography variant="body2" paragraph sx={{ mt: 2 }}>
          <strong>Методы расчета:</strong>
        </Typography>
        <ul>
          <li>Метод прямой капитализации (ПК)</li>
          <li>Метод дисконтированных денежных потоков (ДДП)</li>
        </ul>
      </Paper>
    </Box>
  );
};

export default SettingsPage;
