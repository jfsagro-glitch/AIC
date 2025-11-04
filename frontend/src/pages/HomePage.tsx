import React from 'react';
import { Typography, Box, Card, CardContent, Grid, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HotelIcon from '@mui/icons-material/Hotel';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import BusinessIcon from '@mui/icons-material/Business';
import CalculateIcon from '@mui/icons-material/Calculate';
import UploadFileIcon from '@mui/icons-material/UploadFile';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Добро пожаловать в AI Залоговик
      </Typography>
      <Typography variant="h6" color="text.secondary" paragraph>
        Система автоматизированной оценки коммерческой недвижимости с использованием AI-ассистента
      </Typography>

      <Box sx={{ mb: 4, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<UploadFileIcon />}
          onClick={() => navigate('/upload')}
        >
          Загрузить данные
        </Button>
        <Button
          variant="contained"
          size="large"
          startIcon={<CalculateIcon />}
          onClick={() => navigate('/calculate')}
        >
          Начать расчет
        </Button>
      </Box>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <HotelIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Гостиницы
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Оценка гостиниц категорий 4 и 3 звезды
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <ShoppingCartIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Торговые центры
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Оценка торговых центров и торговых площадей
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Офисные центры
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Оценка офисных центров классов A, B, C
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Методы оценки
        </Typography>
        <Typography variant="body1" paragraph>
          Система использует два основных метода оценки:
        </Typography>
        <Box component="ul" sx={{ pl: 3 }}>
          <li style={{ marginBottom: '0.5rem' }}>
            <strong>Метод прямой капитализации (ПК)</strong> - для быстрой оценки
            на основе текущих доходов
          </li>
          <li style={{ marginBottom: '0.5rem' }}>
            <strong>Метод дисконтированных денежных потоков (ДДП)</strong> - для
            детальной оценки с прогнозом на 5 лет
          </li>
        </Box>
      </Box>

      <Box sx={{ mt: 4, p: 3, bgcolor: 'primary.light', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          Быстрый старт
        </Typography>
        <Typography variant="body2" paragraph>
          1. Загрузите данные о недвижимости в формате Excel или введите вручную
        </Typography>
        <Typography variant="body2" paragraph>
          2. Выберите тип объекта и метод расчета
        </Typography>
        <Typography variant="body2" paragraph>
          3. Получите детальную оценку стоимости с использованием AI-ассистента
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/calculate')}
          sx={{ mt: 2 }}
        >
          Начать оценку
        </Button>
      </Box>
    </Box>
  );
};

export default HomePage;
