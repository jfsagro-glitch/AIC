# ⚡ Быстрый деплой: GitHub Pages + Render

## 📋 За 5 минут

### 1. Настройте GitHub Pages (2 минуты)

1. Откройте репозиторий: https://github.com/jfsagro-glitch/AIC
2. Settings → Pages
3. Source: **Deploy from a branch**
4. Branch: **gh-pages** (создастся автоматически)
5. Folder: **/ (root)**
6. Save

### 2. Добавьте секрет для API (1 минута)

1. Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `REACT_APP_API_URL`
4. Value: `https://aic-backend.onrender.com` (получите после деплоя backend)
5. Add secret

### 3. Деплойте Backend на Render (2 минуты)

1. Откройте [render.com](https://render.com) → Sign up через GitHub
2. New → **Web Service**
3. Connect GitHub → выберите `jfsagro-glitch/AIC`
4. Настройки:
   - **Name:** `aic-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   ```
   DEEPSEEK_API_KEY = ваш_ключ
   DATABASE_URL = (создайте PostgreSQL сначала)
   FRONTEND_URL = https://jfsagro-glitch.github.io/AIC
   ```
6. Create Web Service

### 4. Создайте PostgreSQL на Render (1 минута)

1. New → **PostgreSQL**
2. Name: `aic-db`
3. Plan: Free
4. Create
5. Скопируйте **Internal Database URL**
6. Вставьте в `DATABASE_URL` вашего Web Service

## ✅ Готово!

- **Frontend:** https://jfsagro-glitch.github.io/AIC
- **Backend:** https://aic-backend.onrender.com/docs

---

## 🔄 Автоматический деплой

После настройки:
- **Frontend:** автоматически деплоится при push в `main`
- **Backend:** автоматически деплоится при push в `main` (через Render)

## 📝 Обновление после изменений

Просто сделайте:
```bash
git add .
git commit -m "Update"
git push origin main
```

Все задеплоится автоматически!

