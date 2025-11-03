import React from 'react';
import { Typography, Box, Card, CardContent, Grid } from '@mui/material';
import HotelIcon from '@mui/icons-material/Hotel';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import BusinessIcon from '@mui/icons-material/Business';

const HomePage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Добро пожаловать в AI Залоговик
      </Typography>
      <Typography variant="h6" color="text.secondary" paragraph>
        Система автоматизированной оценки коммерческой недвижимости
      </Typography>

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
        <ul>
          <li>
            <strong>Метод прямой капитализации (ПК)</strong> - для быстрой оценки
            на основе текущих доходов
          </li>
          <li>
            <strong>Метод дисконтированных денежных потоков (ДДП)</strong> - для
            детальной оценки с прогнозом на 5 лет
          </li>
        </ul>
      </Box>
    </Box>
  );
};

export default HomePage;
