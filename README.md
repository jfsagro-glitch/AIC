# AI Залоговик

Система автоматизированной оценки коммерческой недвижимости с использованием AI-ассистента.

## 🏗️ Архитектура

- **Frontend**: React/TypeScript + Material-UI
- **Backend**: Python FastAPI
- **База данных**: PostgreSQL
- **AI интеграция**: DeepSeek API
- **Контейнеризация**: Docker + Docker Compose

## 📋 Поддерживаемые объекты

- Гостиницы (4 и 3 звезды)
- Торговые центры
- Офисные центры (классы A, B, C)

## 📊 Методы оценки

1. **Метод прямой капитализации (ПК)** - для быстрой оценки на основе текущих доходов
2. **Метод дисконтированных денежных потоков (ДДП)** - для детальной оценки с прогнозом на 5 лет

## 🚀 Быстрый старт

> ⚡ **Хотите задеплоить быстро?** См. [QUICK_START.md](./QUICK_START.md) для деплоя за 10 минут!

### Требования

- Docker и Docker Compose (для локального запуска)
- DeepSeek API ключ (получить на [platform.deepseek.com](https://platform.deepseek.com))

### Установка и запуск

1. **Клонирование репозитория**

```bash
git clone https://github.com/jfsagro-glitch/AIC.git
cd AIC
```

2. **Настройка окружения**

Создайте файл `.env` в корне проекта:

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/aic
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

3. **Запуск приложения**

```bash
docker-compose up -d
```

4. **Доступ к приложению**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Документация: http://localhost:8000/docs

## 📁 Структура проекта

```
AIC/
├── frontend/                 # React приложение
│   ├── src/
│   │   ├── components/      # React компоненты
│   │   ├── pages/           # Страницы приложения
│   │   └── App.tsx          # Главный компонент
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI сервер
│   ├── routers/             # API роутеры
│   │   ├── valuation.py     # Расчет стоимости
│   │   ├── ai.py            # AI интеграция
│   │   ├── files.py         # Загрузка файлов
│   │   ├── history.py       # История расчетов
│   │   └── market.py        # Рыночные данные
│   ├── models.py            # Модели данных
│   ├── database.py          # Настройка БД
│   ├── main.py              # Точка входа
│   ├── Dockerfile
│   └── requirements.txt
├── ai_core/                 # Ядро расчетов
│   ├── calculations.py     # Расчетные модули
│   └── constants.py        # Константы и промпты
├── docker-compose.yml       # Docker конфигурация
└── README.md
```

## 🔧 Основные функции

### 1. Загрузка данных

- Загрузка Excel файлов (.xlsx, .xls)
- Автоматическое извлечение данных из таблиц
- Ручной ввод данных через веб-интерфейс

### 2. Расчет стоимости

- Интерактивный расчет с выбором метода (ПК или ДДП)
- Формы ввода данных для разных типов недвижимости
- Отображение детализированных результатов
- Интеграция с AI для оценки недостающих параметров

### 3. AI Ассистент

- Общение с AI в реальном времени
- Автоматическая оценка недостающих параметров
- Валидация результатов расчетов
- Получение рыночных данных

### 4. История расчетов

- Просмотр всех выполненных расчетов
- Фильтрация по типу объекта
- Просмотр деталей каждого расчета
- Удаление записей

### 5. Настройки

- Управление API ключами
- Настройка параметров системы

## 📡 API Endpoints

### Расчет стоимости

- `POST /api/valuation/calculate` - Выполнить расчет стоимости

### AI Ассистент

- `POST /api/ai/conversation` - Общение с AI
- `POST /api/ai/estimate-parameters` - Оценка недостающих параметров
- `POST /api/ai/validate` - Валидация расчета

### Файлы

- `POST /api/files/upload` - Загрузка Excel файлов

### История

- `GET /api/history/` - Получить историю расчетов
- `GET /api/history/{id}` - Получить конкретный расчет
- `DELETE /api/history/{id}` - Удалить расчет

### Рыночные данные

- `GET /api/market/data` - Получить рыночные данные через AI

## 🧮 Параметры расчета по умолчанию

### Ставки капитализации

- Гостиница 4 звезды: 10.75%
- Гостиница 3 звезды: 11.25%
- Торговый центр: 10.5%
- Офисный центр класс A: 13.5%
- Офисный центр класс B: 14.0%
- Офисный центр класс C: 14.5%

### Коэффициенты загрузки

- Гостиницы: 55%
- Торговые центры: 98%
- Офисные центры: 90%

## 🔒 Безопасность

- API ключи хранятся в переменных окружения
- Валидация всех входящих данных
- Логирование всех AI запросов

## 🚀 Деплой в Production

> 🎯 **Рекомендуемый вариант:** Frontend на GitHub Pages + Backend на Render
> 
> См. [DEPLOY_GITHUB_PAGES.md](./DEPLOY_GITHUB_PAGES.md) для детальных инструкций!

### ⭐ Вариант 1: GitHub Pages (Frontend) + Render (Backend) - РЕКОМЕНДУЕТСЯ

#### Frontend на GitHub Pages (Автоматически через Actions)

1. **Включите GitHub Pages:**
   - Settings → Pages → Source: Deploy from a branch → `gh-pages`
   
2. **Добавьте секрет:**
   - Settings → Secrets → Actions → `REACT_APP_API_URL` = URL вашего Render backend

3. **Автоматический деплой:**
   - При push в main автоматически задеплоится на `https://jfsagro-glitch.github.io/AIC`

#### Backend на Render

1. Перейдите на [render.com](https://render.com)
2. New → Web Service → Connect GitHub
3. Root Directory: `backend`
4. Environment Variables:
   - `DEEPSEEK_API_KEY`
   - `DATABASE_URL` (из PostgreSQL сервиса)
   - `FRONTEND_URL` = `https://jfsagro-glitch.github.io/AIC`

**Детальная инструкция:** [DEPLOY_GITHUB_PAGES.md](./DEPLOY_GITHUB_PAGES.md)

### Вариант 2: Vercel (Frontend) + Railway/Render (Backend)

#### Деплой Frontend на Vercel

1. Установите [Vercel CLI](https://vercel.com/cli):
```bash
npm i -g vercel
```

2. Войдите в Vercel:
```bash
vercel login
```

3. Задеплойте frontend:
```bash
cd frontend
vercel
```

4. Настройте переменные окружения в Vercel Dashboard:
   - `REACT_APP_API_URL` - URL вашего backend API

#### Деплой Backend на Railway

1. Перейдите на [Railway.app](https://railway.app)
2. Создайте новый проект из GitHub репозитория
3. Выберите backend директорию
4. Настройте переменные окружения:
   - `DEEPSEEK_API_KEY`
   - `DATABASE_URL` (Railway предоставит PostgreSQL)
   - `FRONTEND_URL` - URL вашего Vercel приложения

#### Деплой Backend на Render

1. Перейдите на [Render.com](https://render.com)
2. Создайте новый Web Service из GitHub репозитория
3. Настройки:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Вариант 2: Heroku (Полный стек)

#### Деплой Backend на Heroku

```bash
# Установите Heroku CLI
heroku login
heroku create aic-backend

# Добавьте PostgreSQL
heroku addons:create heroku-postgresql:mini

# Настройте переменные окружения
heroku config:set DEEPSEEK_API_KEY=your_key
heroku config:set FRONTEND_URL=https://your-frontend.vercel.app

# Деплой
git subtree push --prefix backend heroku main
```

### Вариант 3: Docker Hub + VPS

1. Соберите образы:
```bash
docker build -t your-username/aic-backend ./backend
docker build -t your-username/aic-frontend ./frontend
```

2. Загрузите на Docker Hub:
```bash
docker push your-username/aic-backend
docker push your-username/aic-frontend
```

3. На VPS:
```bash
docker-compose up -d
```

## 📝 Разработка

### Локальная разработка (без Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## 📚 Дополнительная документация

- [DEPLOY_GITHUB_PAGES.md](./DEPLOY_GITHUB_PAGES.md) - ⭐ Деплой на GitHub Pages + Render
- [QUICK_START.md](./QUICK_START.md) - Быстрый старт деплоя (10 минут)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Полное руководство по деплою
- [DEPLOY.md](./DEPLOY.md) - Инструкции по GitHub
- [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md) - Чеклист деплоя
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Руководство по внесению вклада

## 🐛 Решение проблем

### Проблемы с подключением к базе данных

Убедитесь, что PostgreSQL контейнер запущен:
```bash
docker-compose ps
```

### Проблемы с DeepSeek API

Проверьте, что API ключ правильно установлен в `.env` файле:
```bash
echo $DEEPSEEK_API_KEY
```

### Проблемы с портами

Если порты 3000, 8000 или 5432 заняты, измените их в `docker-compose.yml`.

## 📄 Лицензия

Этот проект разработан в рамках задания.

## 👥 Контакты

Репозиторий: https://github.com/jfsagro-glitch/AIC
