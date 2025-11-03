# 🔧 Исправление подключения к базе данных на Render

## Проблема

```
psycopg2.OperationalError: подключение к серверу на "localhost" порт 5432 не удалось
```

Это означает, что `DATABASE_URL` не настроен или использует значение по умолчанию.

## ✅ Решение

### Шаг 1: Создайте PostgreSQL базу данных

1. В Render Dashboard:
   - **New** → **PostgreSQL**
   - **Name:** `aic-db`
   - **Database:** `aic`
   - **User:** `user`
   - **Plan:** Free
   - **Create Database**

2. После создания:
   - Откройте вашу базу данных
   - Скопируйте **Internal Database URL** (НЕ External!)
   - Формат: `postgresql://user:password@hostname:5432/aic`

### Шаг 2: Настройте переменную DATABASE_URL

1. Откройте ваш Web Service (`aic-backend`)
2. Перейдите в **Environment**
3. Добавьте переменную:
   - **Key:** `DATABASE_URL`
   - **Value:** Вставьте **Internal Database URL** из шага 1
4. **Save Changes**

### Шаг 3: Перезапустите сервис

1. **Manual Deploy** → **Clear build cache & deploy**
2. Или подождите автоматического деплоя после push

## 🎯 Проверка

После перезапуска проверьте логи:
- Должно быть: `✅ Database tables created successfully`
- НЕ должно быть ошибок подключения

## ⚠️ Важно

- Используйте **Internal Database URL**, не External
- Убедитесь, что база данных и сервис в одном регионе
- Если используете `render.yaml`, переменная настроится автоматически

## 🔄 Если используете render.yaml

При использовании Blueprint из `render.yaml`:
1. Перейдите в Dashboard → **New** → **Blueprint**
2. Подключите GitHub репозиторий
3. Render автоматически создаст базу и настроит `DATABASE_URL`

---

После настройки все должно работать! 🚀

