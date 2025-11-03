# 📦 Руководство по деплою

## Быстрый деплой за 5 минут

### 1. Frontend на Vercel (Рекомендуется)

1. **Подготовка:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Деплой через Vercel CLI:**
   ```bash
   npm i -g vercel
   vercel login
   vercel --prod
   ```

3. **Или через веб-интерфейс:**
   - Перейдите на [vercel.com](https://vercel.com)
   - Импортируйте репозиторий `jfsagro-glitch/AIC`
   - Root Directory: `frontend`
   - Framework Preset: `Create React App`
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Environment Variables:
     - `REACT_APP_API_URL` = URL вашего backend

### 2. Backend на Railway (Рекомендуется)

1. Перейдите на [railway.app](https://railway.app)
2. Создайте аккаунт через GitHub
3. New Project → Deploy from GitHub repo
4. Выберите репозиторий `jfsagro-glitch/AIC`
5. Добавьте PostgreSQL:
   - New → Database → PostgreSQL
6. Настройте переменные окружения:
   - `DEEPSEEK_API_KEY` = ваш API ключ
   - `DATABASE_URL` = автоматически из PostgreSQL
   - `FRONTEND_URL` = URL вашего Vercel приложения
7. Railway автоматически определит Dockerfile и задеплоит

### 3. Альтернатива: Render.com

#### Backend:
1. Перейдите на [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub → выберите репозиторий
4. Настройки:
   - **Name:** aic-backend
   - **Environment:** Python 3
   - **Root Directory:** backend
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   ```
   DEEPSEEK_API_KEY=your_key
   DATABASE_URL=postgresql://... (Render предоставит)
   FRONTEND_URL=https://your-frontend.vercel.app
   ```

#### PostgreSQL на Render:
1. New → PostgreSQL
2. Выберите план (Free tier доступен)
3. Скопируйте Internal Database URL

## Полный стек на одном сервере (VPS)

### Требования:
- VPS с Docker и Docker Compose
- Домен (опционально)

### Шаги:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/jfsagro-glitch/AIC.git
   cd AIC
   ```

2. **Создайте .env файл:**
   ```bash
   cp env.example .env
   nano .env
   ```
   Заполните:
   ```
   DEEPSEEK_API_KEY=your_key
   DATABASE_URL=postgresql://user:password@db:5432/aic
   FRONTEND_URL=http://your-domain.com
   BACKEND_URL=http://your-domain.com:8000
   ```

3. **Запустите:**
   ```bash
   docker-compose up -d
   ```

4. **Настройте Nginx (опционально):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:3000;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

## GitHub Actions (Автоматический деплой)

Проект уже настроен с GitHub Actions workflows:

- **`.github/workflows/deploy.yml`** - Тестирование и сборка
- **`.github/workflows/deploy-production.yml`** - Сборка Docker образов
- **`.github/workflows/deploy-vercel.yml`** - Автодеплой на Vercel

### Настройка секретов для Vercel:

1. Получите токен на [vercel.com/account/tokens](https://vercel.com/account/tokens)
2. Получите Org ID и Project ID из Vercel проекта
3. В GitHub репозитории:
   - Settings → Secrets and variables → Actions
   - Добавьте:
     - `VERCEL_TOKEN`
     - `VERCEL_ORG_ID`
     - `VERCEL_PROJECT_ID`

## Проверка деплоя

### Frontend:
- Откройте URL вашего Vercel приложения
- Должна загрузиться главная страница

### Backend:
- Проверьте API документацию: `https://your-backend-url.com/docs`
- Health check: `https://your-backend-url.com/health`

### Тестирование:
```bash
# Проверка API
curl https://your-backend-url.com/health

# Проверка Frontend
curl https://your-frontend-url.vercel.app
```

## Обновление после изменений

### Автоматически:
Просто сделайте push в main ветку - GitHub Actions автоматически задеплоит изменения.

### Вручную:

**Frontend (Vercel):**
```bash
cd frontend
vercel --prod
```

**Backend (Railway/Render):**
Изменения автоматически деплоятся при push в main.

## Мониторинг и логи

### Railway:
- Dashboard → ваш проект → Logs

### Render:
- Dashboard → ваш сервис → Logs

### Vercel:
- Dashboard → ваш проект → Logs

## Устранение проблем

### Проблема: Frontend не подключается к Backend

**Решение:**
1. Проверьте `REACT_APP_API_URL` в Vercel
2. Убедитесь, что CORS настроен в backend
3. Проверьте, что backend запущен и доступен

### Проблема: База данных не подключена

**Решение:**
1. Проверьте `DATABASE_URL` в переменных окружения
2. Убедитесь, что PostgreSQL сервис запущен (Railway/Render)
3. Проверьте логи backend

### Проблема: Docker образ не собирается

**Решение:**
```bash
# Локальная проверка
docker build -t test-backend ./backend
docker run -p 8000:8000 test-backend
```

## Бюджетные варианты (Free Tier)

1. **Frontend:** Vercel (бесплатно, неограниченно)
2. **Backend:** Railway или Render (бесплатный tier с ограничениями)
3. **База данных:** Railway PostgreSQL или Render PostgreSQL

## Production рекомендации

1. Используйте платные планы для production
2. Настройте SSL сертификаты (автоматически на Vercel/Railway/Render)
3. Настройте мониторинг (Sentry, LogRocket)
4. Используйте CDN для статики
5. Настройте резервное копирование БД

