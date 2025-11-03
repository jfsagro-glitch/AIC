# 🚀 Деплой: Frontend на GitHub Pages + Backend на Render

## Быстрый старт

### Шаг 1: Настройка GitHub Pages для Frontend

#### Автоматический деплой (Рекомендуется)

1. **Включите GitHub Pages в репозитории:**
   - Перейдите в Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` (будет создана автоматически)
   - Folder: `/ (root)`
   - Нажмите Save

2. **Добавьте секрет для API URL:**
   - Settings → Secrets and variables → Actions
   - New repository secret:
     - Name: `REACT_APP_API_URL`
     - Value: `https://your-backend.onrender.com` (получите после деплоя backend)

3. **Проверьте workflow:**
   - Actions → Deploy Frontend to GitHub Pages
   - Workflow запустится автоматически при push в main
   - После успешного деплоя ваш сайт будет доступен на:
     `https://jfsagro-glitch.github.io/AIC`

#### Ручной деплой (Альтернатива)

```bash
cd frontend
npm install
npm run build

# Установите gh-pages (один раз)
npm install --save-dev gh-pages

# Добавьте в package.json:
# "homepage": "https://jfsagro-glitch.github.io/AIC"

# Деплой
npm run deploy
```

---

### Шаг 2: Настройка Backend на Render

#### Через веб-интерфейс Render

1. **Создайте аккаунт:**
   - Перейдите на [render.com](https://render.com)
   - Sign up через GitHub

2. **Создайте PostgreSQL базу данных:**
   - Dashboard → New → PostgreSQL
   - Name: `aic-db`
   - Database: `aic`
   - User: `user`
   - Plan: Free
   - Region: Frankfurt (или ближайший)
   - Create Database
   - **Скопируйте Internal Database URL**

3. **Создайте Web Service:**
   - Dashboard → New → Web Service
   - Connect GitHub → выберите репозиторий `jfsagro-glitch/AIC`
   - Настройки:
     - **Name:** `aic-backend`
     - **Environment:** `Python 3`
     - **Region:** Frankfurt
     - **Branch:** `main`
     - **Root Directory:** `backend`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** Free

4. **Настройте Environment Variables:**
   ```
   DEEPSEEK_API_KEY = ваш_ключ_от_deepseek
   DATABASE_URL = внутренний_url_от_постгрес (из шага 2)
   FRONTEND_URL = https://jfsagro-glitch.github.io/AIC
   ```

5. **Create Web Service**

6. **Настройте Health Check:**
   - Settings → Health Check Path: `/health`

#### Через render.yaml (Автоматически)

Если вы используете `render.yaml`, Render автоматически создаст все сервисы:

1. Загрузите файл `render.yaml` в корень репозитория (уже загружен)
2. В Render Dashboard:
   - New → Blueprint
   - Connect GitHub → выберите репозиторий
   - Render автоматически создаст все сервисы

---

### Шаг 3: Обновите Frontend URL

После деплоя backend на Render:

1. **Скопируйте URL backend:**
   - Формат: `https://aic-backend.onrender.com`

2. **Обновите секрет в GitHub:**
   - Settings → Secrets and variables → Actions
   - Отредактируйте `REACT_APP_API_URL`
   - Новое значение: `https://aic-backend.onrender.com`

3. **Перезапустите деплой Frontend:**
   - Actions → Deploy Frontend to GitHub Pages → Run workflow

---

## Проверка деплоя

### Frontend (GitHub Pages)
✅ Откройте: `https://jfsagro-glitch.github.io/AIC`
- Должна загрузиться главная страница
- Проверьте, что API запросы идут на Render backend

### Backend (Render)
✅ Откройте: `https://aic-backend.onrender.com/docs`
- Должна открыться документация API
✅ Health check: `https://aic-backend.onrender.com/health`
- Должен вернуться `{"status":"ok"}`

---

## Переменные окружения

### GitHub Secrets (для Frontend)
```
REACT_APP_API_URL=https://aic-backend.onrender.com
```

### Render Environment Variables (для Backend)
```
DEEPSEEK_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@.../aic
FRONTEND_URL=https://jfsagro-glitch.github.io/AIC
```

---

## Обновление после изменений

### Frontend
- Просто сделайте push в main ветку
- GitHub Actions автоматически задеплоит изменения

### Backend
- Push в main → Render автоматически задеплоит
- Или вручную: Render Dashboard → Manual Deploy

---

## Troubleshooting

### Frontend не подключается к Backend

1. **Проверьте CORS в backend:**
   - Убедитесь, что `FRONTEND_URL` правильный
   - Проверьте `backend/main.py` - должен быть в `allow_origins`

2. **Проверьте REACT_APP_API_URL:**
   - Должен быть полный URL: `https://aic-backend.onrender.com`
   - Не используйте trailing slash

### Backend не запускается на Render

1. **Проверьте логи:**
   - Render Dashboard → ваш сервис → Logs

2. **Проверьте переменные окружения:**
   - Все ли они установлены?
   - Правильные ли значения?

3. **Проверьте команду запуска:**
   - Должна быть: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### База данных не подключается

1. **Используйте Internal Database URL:**
   - Render → PostgreSQL → Internal Database URL
   - Не используйте External URL внутри Render

2. **Проверьте переменную DATABASE_URL:**
   - Должна начинаться с `postgresql://`

---

## Преимущества этого подхода

✅ **GitHub Pages:**
- Бесплатный хостинг для статических сайтов
- Автоматический SSL
- Автоматический деплой через Actions
- Неограниченный трафик

✅ **Render:**
- Бесплатный tier для backend
- Автоматический деплой из GitHub
- Встроенный PostgreSQL
- Health checks
- Автоматический SSL

---

## Мониторинг

### GitHub Pages
- Проверьте Actions для статуса деплоя
- Settings → Pages для настроек

### Render
- Dashboard → ваш сервис → Metrics
- Logs доступны в реальном времени
- Health checks автоматически мониторятся

---

## Стоимость

💰 **Полностью бесплатно:**
- GitHub Pages: бесплатно
- Render Free tier: бесплатно (с ограничениями)
- PostgreSQL Free tier: бесплатно

---

Готово! Ваше приложение задеплоено на GitHub Pages (Frontend) и Render (Backend).

