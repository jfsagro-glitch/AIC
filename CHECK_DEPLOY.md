# ✅ Проверка деплоя

## Как проверить, что все работает

### 1. Проверка GitHub Actions

1. Откройте: https://github.com/jfsagro-glitch/AIC/actions
2. Найдите workflow "Deploy Frontend to GitHub Pages"
3. Проверьте статус:
   - ✅ Зеленый значок = успешно
   - ❌ Красный = есть ошибки
   - 🟡 Желтый = выполняется

### 2. Проверка GitHub Pages

1. Откройте: https://github.com/jfsagro-glitch/AIC/settings/pages
2. Проверьте:
   - ✅ Source: GitHub Actions или Deploy from a branch
   - ✅ URL: должен быть указан (например, `https://jfsagro-glitch.github.io/AIC`)

### 3. Проверка секретов

1. Откройте: https://github.com/jfsagro-glitch/AIC/settings/secrets/actions
2. Проверьте наличие секрета:
   - ✅ `REACT_APP_API_URL` должен быть в списке

### 4. Тест деплоя

Если workflow не запустился автоматически:

1. Перейдите: https://github.com/jfsagro-glitch/AIC/actions
2. Выберите "Deploy Frontend to GitHub Pages"
3. Нажмите "Run workflow" → "Run workflow"
4. Дождитесь завершения (2-3 минуты)

### 5. Проверка сайта

После успешного деплоя:
- Откройте: https://jfsagro-glitch.github.io/AIC
- Должна загрузиться главная страница
- Проверьте, что нет ошибок в консоли браузера (F12)

## 🔍 Диагностика проблем

### Если Actions не запускается:
- Проверьте, что файл `.github/workflows/deploy-pages.yml` существует
- Убедитесь, что он в ветке `main`
- Проверьте синтаксис YAML

### Если Pages показывает 404:
- Проверьте, что Pages активированы
- Подождите 1-2 минуты после деплоя
- Очистите кэш браузера (Ctrl+F5)

### Если секрет не работает:
- Убедитесь, что имя точно `REACT_APP_API_URL`
- Проверьте, что значение - полный URL (начинается с `https://`)
- Перезапустите workflow после изменения секрета

---

**Проверьте все пункты выше и сообщите, если что-то не работает!** 🔍

