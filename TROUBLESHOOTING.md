# 🔧 Устранение проблем

## Ошибка: "Key is invalid. You must supply a key in OpenSSH public key format"

Эта ошибка возникает, если вы пытаетесь добавить SSH ключ, но для GitHub Pages через Actions **SSH ключи НЕ нужны!**

### ✅ Правильный способ активации GitHub Pages

#### Вариант 1: GitHub Actions (Рекомендуется)

1. **НЕ добавляйте SSH ключи!**
2. Просто перейдите: **Settings** → **Pages**
3. **Source:** выберите **GitHub Actions**
4. Если опции нет:
   - Сначала запустите workflow вручную:
     - **Actions** → **Deploy Frontend to GitHub Pages** → **Run workflow**
   - Или используйте Вариант 2

#### Вариант 2: Deploy from branch

1. **Settings** → **Pages**
2. **Source:** **Deploy from a branch**
3. **Branch:** `gh-pages`
4. **Folder:** `/ (root)`
5. **Save**

### ❌ Что НЕ нужно делать

- ❌ Добавлять SSH ключи
- ❌ Настраивать Deploy keys
- ❌ Использовать Personal Access Tokens для Pages

### ✅ Что нужно сделать

1. Просто активировать Pages в Settings
2. Добавить секрет `REACT_APP_API_URL` (это не SSH ключ!)
3. Workflow автоматически задеплоит при push

## Другие частые проблемы

### Проблема: GitHub Actions не запускается

**Решение:**
1. Проверьте, что workflow файл существует: `.github/workflows/deploy-pages.yml`
2. Убедитесь, что файл в формате YAML (правильные отступы)
3. Проверьте Actions → All workflows
4. Запустите вручную: Actions → Deploy Frontend to GitHub Pages → Run workflow

### Проблема: Pages показывает 404

**Решение:**
1. Проверьте, что Pages активированы в Settings
2. Проверьте Actions - должен быть успешный деплой
3. Подождите 1-2 минуты после деплоя
4. Обновите страницу (Ctrl+F5)

### Проблема: "Workflow not found"

**Решение:**
1. Убедитесь, что файл `.github/workflows/deploy-pages.yml` существует
2. Проверьте, что он закоммичен в `main` ветку
3. Сделайте новый push, если нужно

### Проблема: Секрет не работает

**Решение:**
1. Settings → Secrets and variables → Actions
2. Убедитесь, что секрет называется точно `REACT_APP_API_URL`
3. Значение должно быть полным URL: `https://aic-backend.onrender.com`
4. После изменения секрета перезапустите workflow

---

## 🆘 Нужна помощь?

1. Проверьте логи в **Actions** → выберите workflow → посмотрите ошибки
2. Убедитесь, что все файлы загружены на GitHub
3. Проверьте, что Pages активированы в Settings

---

**Главное:** Для GitHub Pages НЕ нужны SSH ключи! Просто активируйте Pages в Settings.

