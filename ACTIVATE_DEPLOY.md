# 🚀 Активация деплоя - Финальные шаги

## ✅ Что уже готово

- ✅ Все файлы загружены на GitHub: https://github.com/jfsagro-glitch/AIC
- ✅ GitHub Actions настроены для автоматического деплоя
- ✅ Конфигурация для Render готова
- ✅ Код исправлен и работает

## 📋 Что нужно сделать СЕЙЧАС

### 1. Активировать GitHub Pages (Frontend)

**Вариант A: GitHub Actions (Рекомендуется)**

1. Перейдите на GitHub: https://github.com/jfsagro-glitch/AIC
2. **Settings** → **Pages** (в левом меню)
3. **Source:** выберите **GitHub Actions**
   - Если опции нет, сначала нужно запустить workflow один раз
   - Или используйте Вариант B ниже
4. Нажмите **Save**

**Вариант B: Branch (Если Actions не работает)**

1. **Settings** → **Pages**
2. **Source:** **Deploy from a branch**
3. **Branch:** выберите `gh-pages` (создастся автоматически после первого деплоя)
4. **Folder:** `/ (root)`
5. **Save**

> ⚠️ **НЕ используйте SSH ключи!** GitHub Pages работает автоматически через Actions или ветку.

### 2. Добавить секрет для API URL

1. В том же репозитории: **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. **Name:** `REACT_APP_API_URL`
4. **Value:** `https://aic-backend.onrender.com` (URL вашего Render backend)
5. **Add secret**

### 3. Задеплоить Backend на Render

Следуйте инструкциям в [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) или [DEPLOY_GITHUB_PAGES.md](./DEPLOY_GITHUB_PAGES.md)

## 🎯 После активации

### Frontend автоматически задеплоится:
- При push в `main` ветку
- GitHub Actions соберет и задеплоит на Pages
- URL: `https://jfsagro-glitch.github.io/AIC`

### Backend нужно настроить вручную:
- Создать PostgreSQL на Render
- Создать Web Service на Render
- Настроить Environment Variables

## 📊 Проверка статуса

### GitHub Actions
- Проверьте: https://github.com/jfsagro-glitch/AIC/actions
- Должны запуститься workflow при изменении frontend

### GitHub Pages
- После активации проверьте: https://jfsagro-glitch.github.io/AIC
- Должна загрузиться главная страница

## 🔗 Полезные ссылки

- Репозиторий: https://github.com/jfsagro-glitch/AIC
- Actions: https://github.com/jfsagro-glitch/AIC/actions
- Settings: https://github.com/jfsagro-glitch/AIC/settings
- Pages: https://github.com/jfsagro-glitch/AIC/settings/pages

---

**Готово к деплою!** Просто активируйте GitHub Pages и настройте Render. 🚀

